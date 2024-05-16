#from Game_State import Game_State
#from Gin_Oracle import Gin_Oracle
import random
from Node import Node
import pandas as pd
import keras
from NeuralNetManager import NeuralNetManager

class DeepLearningCFR:
    def __init__(self):
        self.strategies = None
        self.regret_sum = {}
        self.strategy_sum = {}
        self.best_possible_utility = 70
        self.end_states_dist = []
        self.state = None

        self.nn_manager = NeuralNetManager()
        self.discard_model = keras.models.load_model("discard_phase_model.h5")
        self.draw_model = keras.models.load_model("draw_binary_model.h5")
    
    def insert_strategy_via_index(self, value, index):
        #get all the strategy rows
        column_names = self.strategies.columns
        #print("Column names: ", column_names)
        column_to_insert = column_names[index]
        #print("Column to insert: ", column_to_insert)
        self.strategies[column_to_insert] = value

    def resolve(self, state, EndStage, EndDepth, iterations, smallDeck = True, return_number_value = False):
        #Create the node three
        root = Node(state, None)
        root.create_children_tree(root, EndDepth)
        root.game_state.print_state()
        stage = root.game_state.state
        print("Stage: ", stage)

        if stage == "draw":
            #Important that theese strategies are in the same order as it is in the game_state
            self.strategies = pd.DataFrame({"discard": [0], "random": [0]})
        elif stage == "discard":
            if smallDeck:
                cards_names = []
                cards = root.game_state.main_player_hand.cards
                for i in range(len(cards)):
                    if cards[i].just_drew is False:
                        cards_names.append(cards[i].__str__())
                self.strategies = pd.DataFrame(columns = cards_names, index = list(range(len(root.children)))).fillna(0)

        #for i in range(iterations):
        self.traverse(root, EndStage, EndDepth)
        #self.strategies = self.update_strategies()
        print(self.strategies)

        if return_number_value:
            print("Returning number value")
            print(self.strategies.max(axis=1)[0])
            return self.strategies.max(axis=1)[0]

        best_strategy = self.strategies.idxmax(axis=1)[0]
        if (self.strategies.at[0, best_strategy] == 0).all():
            if stage == "draw":
                best_strategy = "random"
            else:
            #Choose a random card to discard
                random_index = random.randint(0, len(root.children) - 1)
                best_strategy = self.strategies.columns[random_index]
                
        print("Best strategy: ", best_strategy)

        if stage == "discard":
            for i in range(len(root.game_state.main_player_hand.cards)):
                if root.game_state.main_player_hand.cards[i].__str__() == best_strategy:
                    best_strategy = i + 1
                    break
        

        return best_strategy
    
    def traverse(self, node, EndStage, EndDepth):
        #print("Traversing")
        if node.depth == EndDepth or node.game_state.state == EndStage or node.game_state.state == "knock":
            #print("End reached")
            if node.game_state.state == "knock":
                print("Knock")
                return 100
            utility = self.calculate_total_utility(node)
            return utility
        
        if node.depth != 0:
            states = node.children
            utilities = []
            for s in states:
                utility = self.traverse(s, EndStage, EndDepth)
                utilities.append(utility)

            if node.game_state.main_player_index == node.game_state.turn_index or node.game_state.state == "discard":
                best_utility = max(utilities)
            
            else:
                self.basyian_update(node)
                best_utility = 0
                for i in range(len(utilities)):
                    u = utilities[i] * states[i].game_state.probability
                    best_utility += u
                    #print("Best utility: ", best_utility)
                    #print("Probability: ", states[i].game_state.probability)
                    
            return best_utility
        
        else:
            for i in range (len(node.children)):
                utility = self.traverse(node.children[i], EndStage, EndDepth)
                self.insert_strategy_via_index(utility, i)

            return 0


    #TODO: test if this makes the bot better
    def basyian_update(self, node):
        other_player_utilities = []
        for i in range(len(node.children)):
            state = node.children[i].game_state
            other_player_utility = 0

            for j in range(len(state.opponent_category_dist)):
                other_player_utility += state.opponent_category_dist[j]
            
            other_player_utilities.append(other_player_utility)
        
        for i in range(len(node.children)):
            state = node.children[i].game_state
            tot_sum = sum(other_player_utilities)
            if tot_sum == 0:
                state.probability = 1/len(other_player_utilities)
            else:
                state.probability = other_player_utilities[i] / sum(other_player_utilities)
        return


    def calculate_total_utility(self, node):
        #Deadwood is better the lower it is, therefore we subtract it from 70, which is the highest possible deadwood
        state = node.game_state
        
        #if state.main_player_index == state.turn_index:
        #    if stage == "draw":
        #        print("Draw, main player turn")
        #        return self.calculate_total_utility(node.parent)
        #    elif stage == "discard":
        #        print("Discard, main player turn")
        #else:
        #    print("Opponent turn")
        #    return self.calculate_total_utility(node.parent)


        encoded_data = self.get_one_hot_encoding(state.main_player_hand.cards, state.discard_pile, state.top_card_discard_pile, state.opponent_known_cards)
        prediction = self.discard_model.predict(encoded_data, verbose = 0)

        return prediction[0][0]
    
    def get_one_hot_encoding(self, hand_cards, discard_pile, top_of_discard_pile, known_cards):

        #Convert the cards to one hot encoding
        hand_cards_one_hot = [0] * self.nn_manager.bits
        phantom_counter = 0
        for i in range(len(hand_cards)):
            if hand_cards[i].isPhantom:
                hand_cards_one_hot[self.nn_manager.card_to_value_mapping["Phantom Card"] + phantom_counter] = 1
                phantom_counter += 1
            else:
                hand_cards_one_hot[self.nn_manager.card_to_value_mapping[str(hand_cards[i])]] = 1


        #Discard pile
        discard_pile_one_hot = [0] * self.nn_manager.bits
        for i in range(len(discard_pile)):
            discard_pile_one_hot[self.nn_manager.card_to_value_mapping[str(discard_pile[i])]] = 1
        
        #Top of discard pile
        top_of_discard_pile_one_hot = [0] * self.nn_manager.bits
        top_of_discard_pile_one_hot[self.nn_manager.card_to_value_mapping[str(top_of_discard_pile)]] = 1

        #Known cards
        known_cards_one_hot = [0] * self.nn_manager.bits
        for i in range(len(known_cards)):
            known_cards_one_hot[self.nn_manager.card_to_value_mapping[str(known_cards[i])]] = 1
        

        return [[hand_cards_one_hot] + [discard_pile_one_hot] + [top_of_discard_pile_one_hot] + [known_cards_one_hot]]

    def knocking_strategy_rule_based(self, state):
            hand_evaluator = state.oracle.hand_evaluator
            deadwood, melds = hand_evaluator.get_hand_score(state.main_player_hand, True)
            if deadwood == 0:
                return "y"
            
            if state.turn_number > 8:
                return "n"
            
            hit_cards = state.oracle.get_hit_cards(state.main_player_hand, state.opponent_known_cards, state.discard_pile)
            if len(hit_cards) > 2:
                unmelded_cards_count = 0
                for c in state.main_player_hand.cards:
                    if c in melds:
                        continue
                    unmelded_cards_count += 1
                
                if unmelded_cards_count <= 1:
                    return "n"
                
                if unmelded_cards_count > 3 and deadwood < 6:
                    return "n"
            
            return "y"

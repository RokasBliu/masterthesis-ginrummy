import random
from GRONode import GRONode
import pandas as pd
from HandEvaluator import HandEvaluator

class GROCFR:
    def __init__(self):
        self.strategies = None
        self.regret_sum = {}
        self.strategy_sum = {}
        self.best_possible_utility = 70
        self.end_states_dist = []
    
    def insert_strategy_via_index(self, value, index):
        column_names = self.strategies.columns
        column_to_insert = column_names[index]
        self.strategies[column_to_insert] = value

    def resolve(self, state, EndStage, EndDepth, iterations, smallDeck = True):
        #Create the node three
        root = GRONode(state, None)
        root.create_children_tree(root, EndDepth)
        #root.game_state.print_state()
        stage = root.game_state.state
        print("Stage: ", stage)

        if stage == "draw":
            #Important that these strategies are in the same order as it is in the game_state
            self.strategies = pd.DataFrame({"discard": [0], "random": [0]})
        elif stage == "discard":
            cards_names = []
            cards = root.game_state.main_player_hand.cards
            for i in range(len(cards)):
                if cards[i].just_drew is False:
                    cards_names.append(cards[i].__str__())
            self.strategies = pd.DataFrame(columns = cards_names, index = list(range(len(root.children)))).astype(float).fillna(0)

        self.traverse(root, root, EndStage, EndDepth)
        print(self.strategies)
        best_strategy = self.strategies.idxmax(axis=1)[0]
        if self.strategies.at[0, best_strategy] == 0:
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
    
    def traverse(self, node, root, EndStage, EndDepth):
        if node.depth == EndDepth or node.game_state.state == EndStage or node.game_state.state == "knock":
            if node.game_state.state == "knock":
                print("Knock")
                return 100
            utility = self.calculate_total_utility(node, root)
            return utility
        
        if node.depth != 0:
            states = node.children
            utilities = []
            for s in states:
                utility = self.traverse(s, root, EndStage, EndDepth)
                utilities.append(utility)

            if node.game_state.main_player_index == node.game_state.turn_index or node.game_state.state == "discard":
                best_utility = max(utilities)
            else:
                self.basyian_update(node)
                best_utility = 0
                for i in range(len(utilities)):
                    u = utilities[i] * states[i].game_state.probability
                    best_utility += u
                    
            return best_utility
        else:
            for i in range (len(node.children)):
                utility = self.traverse(node.children[i], root, EndStage, EndDepth)
                self.insert_strategy_via_index(utility, i)

            return 0

    def update_strategies(self):
        return

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


    def calculate_total_utility(self, node, root):
        #Deadwood is better the lower it is, therefore we subtract it from 70, which is the highest possible deadwood
        main_player_exp_deadwood = node.game_state.oracle.get_expected_util_sample(node.game_state.main_player_hand)
        hand_evaluator = HandEvaluator()
        exp_p1_utility = hand_evaluator.get_hand_score(root.game_state.main_player_hand) - main_player_exp_deadwood
        exp_p2_utility_dist = node.game_state.opponent_category_dist
        exp_p2_utility_sum = 0
        for i in range(len(exp_p2_utility_dist)):
            exp_p2_utility_sum += exp_p2_utility_dist[i]

        tot_exp_utility = exp_p1_utility - exp_p2_utility_sum
        if tot_exp_utility < 0:
            tot_exp_utility = 0
        #print("Total expected utility: ", tot_exp_utility)
        return tot_exp_utility
    
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


                

            

            
            
            

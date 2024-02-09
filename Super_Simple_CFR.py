#from Game_State import Game_State
#from Gin_Oracle import Gin_Oracle
from copy import deepcopy
from Node import Node
import pandas as pd

class Super_Simple_CFR:
    def __init__(self):
        self.strategies = None
        self.regret_sum = {}
        self.strategy_sum = {}
        self.best_possible_utility = 70
        self.end_states_dist = []
    
    def insert_strategy_via_index(self, value, index):
        #get all the strategy rows
        column_names = self.strategies.columns
        #print("Column names: ", column_names)
        column_to_insert = column_names[index]
        #print("Column to insert: ", column_to_insert)
        self.strategies[column_to_insert] = value

    def resolve(self, state, EndStage, EndDepth, iterations, smallDeck = True):
        #Create the node three
        root = Node(state, None)
        root.create_children_tree(root, EndDepth)
        root.game_state.print_state()
        stage = root.game_state.state
        print("Stage: ", stage)

        if stage == "draw":
            #Important that theese strategies are in the same order as it is in the game_state
            self.strategies = pd.DataFrame({"discard": [0], "random": [0]})
            #print("Strategies: ", self.strategies)
            #print("Strategies columns: ", self.strategies.columns)
        elif stage == "discard":
            if smallDeck:
                cards_names = []
                cards = root.game_state.main_player_hand.cards
                for i in range(len(cards)):
                    cards_names.append(cards[i].__str__())
                self.strategies = pd.DataFrame(columns = cards_names, index = list(range(len(root.children)))).fillna(0)

        #print("Children count: ", root.children_count)
        #for i in range(iterations):
        self.traverse(root, EndStage, EndDepth)
        #self.strategies = self.update_strategies()
        print(self.strategies)
        best_strategy = self.strategies.idxmax(axis=1)[0]
        
        print("Best strategy: ", best_strategy)

        if stage == "discard":
            return self.strategies.columns.get_loc(best_strategy) + 1
        

        return best_strategy
    
    def traverse(self, node, EndStage, EndDepth):
        #print("Traversing")
        if node.depth == EndDepth or node.game_state.state == EndStage:
            #print("End reached")
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
                    
            return best_utility
        
        else:
            for i in range (len(node.children)):
                utility = self.traverse(node.children[i], EndStage, EndDepth)
                self.insert_strategy_via_index(utility, i)

            return 0

                

    
    def update_strategies(self):
        return

    def basyian_update(self, node):
        return


    def calculate_total_utility(self, node):
        #Deadwood is better the lower it is, therefore we subtract it from 70, which is the highest possible deadwood
        main_player_exp_deadwood = node.game_state.oracle.get_expected_utility(node.game_state.main_player_hand)
        exp_p1_utility = node.game_state.main_player_deadwood - main_player_exp_deadwood
        exp_p2_utility_dist = node.game_state.opponent_category_dist
        exp_p2_utility_sum = 0
        for i in range(len(exp_p2_utility_dist)):
            exp_p2_utility_sum += exp_p2_utility_dist[i]

        tot_exp_utility = exp_p1_utility - exp_p2_utility_sum
        if tot_exp_utility < 0:
            tot_exp_utility = 0
        #print("Total expected utility: ", tot_exp_utility)
        return tot_exp_utility

"""def main():
    oracle = Gin_Oracle()
    #game.start_new_game()
    #start_state = Game_State(game, "draw")
    #root = Node(start_state)
    #root.create_children()
    #start_state = root.children[0].game_state
    game, known_cards, stage = oracle.create_random_game()
    start_state = Game_State(game, stage, known_cards)
    depth = 10
    resolver = Super_Simple_CFR()
    best = resolver.resolve(start_state, "end_game", depth, 1)
    print("Best", best)
        
if __name__ == "__main__":
        main()"""
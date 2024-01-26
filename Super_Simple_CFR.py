from Node import Node
import pandas as pd
class Super_Simple_CFR:
    def __inti__(self):
        self.strategies = None
        self.regret_sum = {}
        self.strategy_sum = {}
    
    def resolve(self, state, EndStage, EndDepth, iterations, smallDeck = True):
        #Create the node three
        root = Node(state, None)
        root.create_children_tree(root, EndDepth)

        if state == "draw":
            self.strategies = pd.DataFrame(columns = ["random_card", "discard_pile"])
        elif state == "discard":
            if smallDeck:
                self.strategies = pd.DataFrame(columns = root.game_state.main_player_hand.cards)

        #print("Children count: ", root.children_count)
        #for i in range(iterations):
        self.traverse(root, EndStage, EndDepth)
        self.strategies = self.update_strategies()
    
    def traverse(self, node, EndStage, EndDepth):
        return
    
    def update_strategies(self):
        return


    
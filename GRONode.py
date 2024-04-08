from copy import deepcopy
from HandEvaluator import HandEvaluator
import numpy as np

class GRONode: 
    def __init__(self, game_state, parent=None):
        self.game_state = game_state
        self.parent = parent
        self.children = []
        self.action = None
        self.depth = 0
        self.children_count = 0
        self.probability = 1
        if parent != None:
            self.depth = parent.depth + 1

    def create_children(self):
        if self.game_state.state == "draw":
            #Draw from discard pile          
            new_state = deepcopy(self.game_state)
            child = GRONode(new_state, self)                
            child.game_state.draw_from_discard_pile()
            self.children.append(child)

            new_state = deepcopy(self.game_state)
            child = GRONode(new_state, self)
            child.game_state.draw_card()
            self.children.append(child)
        
        elif self.game_state.state == "discard":
            hand_ev = HandEvaluator()
            #Make states for each card in hand, exluding cards in melds
            if self.game_state.main_player_index == self.game_state.turn_index:
                # cards_not_in_melds = self.game_state.main_player_hand.cards
                cards_not_in_melds = []
                best_meld = hand_ev.find_best_meld(self.game_state.main_player_hand)
                if best_meld is not None:
                    for card in self.game_state.main_player_hand.cards:
                        if card not in best_meld:
                            cards_not_in_melds.append(card)
                else:
                    cards_not_in_melds = self.game_state.main_player_hand.cards
                #np.setdiff1d(self.game_state.main_player_hand.cards, hand_ev.find_best_meld(self.game_state.main_player_hand), False).tolist()
                for c in cards_not_in_melds:
                    if c.just_drew is False:
                        new_state = deepcopy(self.game_state)
                        child = GRONode(new_state, self)
                        child.game_state.discard_from_hand(c)
                        self.children.append(child)

            else:
                new_state = deepcopy(self.game_state)
                child = GRONode(new_state, self)
                child.game_state.discard_from_hand()
                self.children.append(child)
 
        else: #self.game_state.state == "end_game"
            return

    def create_children_tree(self, node, depth):
        if depth == 0:
            return
        else:
            node.create_children()
            self.children_count += len(node.children)
            for c in node.children:             
                c.create_children_tree(c, depth - 1)
        
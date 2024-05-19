from copy import deepcopy
import keras
from NeuralNetManager import NeuralNetManager

class Node: 
    def __init__(self, game_state, parent=None):
        self.game_state = game_state
        self.parent = parent
        self.children = []
        self.action = None
        self.depth = 0
        self.children_count = 0
        self.probability = 1
        self.just_drew_from_discard_pile = False
        if parent != None:
            self.depth = parent.depth + 1

        
    def create_children(self):
        #self.game_state.print_state()
        #print("Depth: ", self.depth)
        if self.game_state.state == "draw":
            #Draw from discard pile'
            self.just_drew_from_discard_pile = True
            new_state = deepcopy(self.game_state)
            child = Node(new_state, self)                
            child.game_state.draw_from_discard_pile()
            self.children.append(child)

            new_state = deepcopy(self.game_state)
            child = Node(new_state, self)
            child.game_state.draw_card()
            self.children.append(child)
        
        elif self.game_state.state == "discard":
            #Make states for each card in hand
            if self.game_state.main_player_index == self.game_state.turn_index:
                for c in self.game_state.main_player_hand.cards:
                    if c.just_drew is False:
                        new_state = deepcopy(self.game_state)
                        child = Node(new_state, self)
                        child.game_state.discard_from_hand(c)
                        self.children.append(child)

            else:
                new_state = deepcopy(self.game_state)
                child = Node(new_state, self)
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
    
    def get_one_hot_encoding(self, hand_cards, discard_pile, top_of_discard_pile, known_cards, nn_manager):

        #Convert the cards to one hot encoding
        hand_cards_one_hot = [0] * nn_manager.bits
        phantom_counter = 0
        for i in range(len(hand_cards)):
            if hand_cards[i].isPhantom:
                hand_cards_one_hot[nn_manager.card_to_value_mapping["Phantom Card"] + phantom_counter] = 1
                phantom_counter += 1
            else:
                hand_cards_one_hot[nn_manager.card_to_value_mapping[str(hand_cards[i])]] = 1


        #Discard pile
        discard_pile_one_hot = [0] * nn_manager.bits
        for i in range(len(discard_pile)):
            discard_pile_one_hot[nn_manager.card_to_value_mapping[str(discard_pile[i])]] = 1
        
        #Top of discard pile
        top_of_discard_pile_one_hot = [0] * nn_manager.bits
        top_of_discard_pile_one_hot[nn_manager.card_to_value_mapping[str(top_of_discard_pile)]] = 1

        #Known cards
        known_cards_one_hot = [0] * nn_manager.bits
        for i in range(len(known_cards)):
            known_cards_one_hot[nn_manager.card_to_value_mapping[str(known_cards[i])]] = 1
        

        return [[hand_cards_one_hot] + [discard_pile_one_hot] + [top_of_discard_pile_one_hot] + [known_cards_one_hot]]
from copy import deepcopy

class Node: 
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
        #self.game_state.print_state()
        #print("Depth: ", self.depth)
        if self.game_state.state == "draw":
            #Draw from discard pile          
            new_state = deepcopy(self.game_state)
            child = Node(new_state, self)                
            child.game_state.draw_from_discard_pile()

            self.children.append(child)
            child.game_state.print_state()
            #print("Depth: ", child.depth)

            #Draw from deck
            # deck = Deck()
            # deck.make_smaller_deck()
            # for c in self.game_state.main_player_hand.cards:
            #     if not c.isPhantom:
            #         deck.remove(c)
            # for c in self.game_state.opponent_known_cards:
            #     if not c.isPhantom:
            #         deck.remove(c)
            # for c in self.game_state.discard_pile:
            #     if not c.isPhantom:
            #         deck.remove(c)

            new_state = deepcopy(self.game_state)
            child = Node(new_state, self)
            child.game_state.draw_card()
            self.children.append(child)
            child.game_state.print_state()
            #print("Depth: ", child.depth)
        
        elif self.game_state.state == "discard":
            #Make states for each card in hand
            if self.game_state.main_player_index == self.game_state.turn_index:
                for c in self.game_state.main_player_hand.cards:
                    new_state = deepcopy(self.game_state)
                    child = Node(new_state, self)
                    child.game_state.discard_from_hand(c)
                    self.children.append(child)
                    #child.game_state.print_state()
                    #print("Depth: ", child.depth)
            else:
                new_state = deepcopy(self.game_state)
                child = Node(new_state, self)
                child.game_state.discard_from_hand()
                self.children.append(child)
                #child.game_state.print_state()
                #print("Depth: ", child.depth)


        elif self.game_state.state == "knock":
            #Can either knock or not knock
            new_state = deepcopy(self.game_state)
            child = Node(new_state, self)
            child.game_state.knock()
            self.children.append(child)
            #child.game_state.print_state()
            #print("Depth: ", child.depth)

            if self.game_state.main_player_deadwood > 0:
                new_state = deepcopy(self.game_state)
                #child = Node(new_state, self)
                #child.game_state.state = "draw"
        
        elif self.game_state.state == "end_game":
            return

    def create_children_tree(self, node, depth):
        if depth == 0:
            return
        else:
            node.create_children()
            self.children_count += len(node.children)
            for c in node.children:             
                c.create_children_tree(c, depth - 1)
        
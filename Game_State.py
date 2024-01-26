class Game_State(object):
    def __init__(self, game, state):
        self.main_player = game.players[game.turn_index]
        self.main_player_index = game.turn_index
        self.main_player_hand = self.main_player.hand

        self.turn_index = game.turn_index
        #self.current_player = game_state.players[self.turn_index]
        self.round_number = game.round_number

        self.state = state

        self.main_player_deadwood = self.main_player.hand.get_hand_score()
        self.main_player_score = self.main_player.score

        self.other_player_score = game.players[(self.turn_index + 1) % 2].score
        self.discard_pile = game.discard_pile
        self.top_card_discard_pile = self.discard_pile[-1]

        self.known_cards = []

    def draw_from_discard_pile(self):
        if self.main_player_index == self.turn_index:
            self.main_player_hand.add(self.top_card_discard_pile)
        else:
            self.known_cards.append(self.top_card_discard_pile)
        
        self.discard_pile.pop()
        self.state = "discard"

        
    def draw_card(self, card):
        if self.main_player_index == self.turn_index:
            self.main_player_hand.add(card)

        self.state = "discard"
    
    def discard_from_hand(self, card=None):
        self.state = "draw"
        if self.main_player_index == self.turn_index and card is not None:
            self.main_player_hand.cards.remove(card)  
            self.main_player_deadwood = self.main_player_hand.get_hand_score()
            if self.main_player_deadwood <= 10:
                self.state = "knock"
        else:
            if card in self.known_cards:
                self.known_cards.remove(card)

        if card is not None:
            self.discard_pile.append(card)
        
        self.turn_index = (self.turn_index + 1) % 2
        if self.turn_index == 0:
            self.round_number += 1

    def knock(self):
        self.state = "end_game"
    
    def print_state(self):
        print("--------------------")
        print("State: ", self.state)
        print("Round number: ", self.round_number)
        print("Main player: ", self.main_player.name)
        print("Main player's hand: ", self.main_player_hand)
        print("Main player's deadwood: ", self.main_player_deadwood)
        print("Discard pile: ", self.discard_pile)
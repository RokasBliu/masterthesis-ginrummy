from Deck import Deck
from Card import Card
class Game_State(object):
    def __init__(self, game, state, opponent_known_cards=[]):
        self.main_player = game.players[game.turn_index]
        self.main_player_index = game.turn_index
        self.main_player_hand = self.main_player.hand

        self.turn_index = game.turn_index
        #self.current_player = game_state.players[self.turn_index]
        self.round_number = game.round_number

        self.state = state

        self.main_player_deadwood = self.main_player.hand.get_hand_score()
        self.main_player_expected_utility = self.main_player_deadwood
        self.main_player_score = self.main_player.score

        self.other_player_score = game.players[(self.turn_index + 1) % 2].score
        self.discard_pile = game.discard_pile
        self.top_card_discard_pile = self.discard_pile[-1]

        self.opponent_known_cards = opponent_known_cards
        self.rand_card_dist = []

        #Calculate random cards available
        rand_deck = Deck()
        rand_deck.make_smaller_deck()
        print("Random deck: ", rand_deck)
        cards_available_counter = 0
        
        for i in range(len(rand_deck)):
            if rand_deck[i] in self.main_player_hand.cards or rand_deck[i] in self.opponent_known_cards or rand_deck[i] in self.discard_pile:
                rand_deck[i] = 0
            else:
                rand_deck[i] = 1
                cards_available_counter += 1
        
        for r in rand_deck:
            self.rand_card_dist.append(r / cards_available_counter)
        
        print("Random card distribution: ", self.rand_card_dist)
        
        

    def draw_from_discard_pile(self):
        if self.main_player_index == self.turn_index:
            self.main_player_hand.add(self.top_card_discard_pile)
        else:
            self.opponent_known_cards.append(self.top_card_discard_pile)
            #TODO Adjust "probability score" of opponent, because it did draw from the discard pile
        
        self.discard_pile.pop()
        self.state = "discard"

        
    def draw_card(self):
        if self.main_player_index == self.turn_index:
            #Adding a random card to hand
            new_card = Card("", "")
            new_card.make_phantom_card(self.rand_card_dist)
            self.main_player_hand.add(new_card)
        
        #TODO Adjust "probability score" of opponent, because it did not draw from the discard pile

        self.state = "discard"
    
    def discard_from_hand(self, card=None):
        if self.main_player_index == self.turn_index and card is not None:
            
            self.main_player_hand.cards.remove(card)
            has_phantom = False
            for c in self.main_player_hand.cards:
                if c.isPhantom:
                    has_phantom = True
                    break
            
            if has_phantom:
                print("Has phantom")
                #TODO - Implement get expected value from hand with phantom cards
                    
            else:  
                self.main_player_deadwood = self.main_player_hand.get_hand_score()

            #self.main_player_expected_utility = self.oracle.get_expected_utility()
            self.state = "draw"

            #if self.main_player_expected_utility <= 10:
            #    self.state = "knock"

        else:
            card = Card("", "").make_phantom_card(self.rand_card_dist)

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
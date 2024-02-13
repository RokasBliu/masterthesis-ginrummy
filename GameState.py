from Deck import Deck
from Card import Card
from GinOracle import GinOracle
from Action import Action
import numpy as np
class GameState(object):
    def __init__(self, game, state, opponent_known_cards=[]):
        self.main_player = game.players[game.turn_index]
        self.main_player_index = game.turn_index
        self.main_player_hand = self.main_player.hand
        self.deck_size = len(game.deck)

        self.turn_index = game.turn_index
        #self.current_player = game_state.players[self.turn_index]
        self.round_number = game.round_number

        self.state = state
        self.probability = 1

        self.main_player_deadwood = self.main_player.hand.get_hand_score()
        self.main_player_expected_utility = self.main_player_deadwood
        self.main_player_score = self.main_player.score

        self.other_player_score = game.players[(self.turn_index + 1) % 2].score
        self.discard_pile = game.discard_pile
        if len(self.discard_pile) > 0:
            self.top_card_discard_pile = self.discard_pile[-1]

        self.opponent_known_cards = opponent_known_cards
        self.opponent_category_dist = np.zeros(7) #TODO: Make this more accurate
        self.rand_card_dist = []
        self.oracle = GinOracle()
        self.action = None

        #Calculate random cards available
        rand_deck = Deck()
        rand_deck.make_smaller_deck()
        cards_available_counter = 0
        
        for i in range(len(rand_deck)):
            if rand_deck[i] in self.main_player_hand.cards or rand_deck[i] in self.opponent_known_cards or rand_deck[i] in self.discard_pile:
                rand_deck[i] = 0
            else:
                rand_deck[i] = 1
                cards_available_counter += 1
        
        for r in rand_deck:
            self.rand_card_dist.append(r / cards_available_counter)
        
        #print("Random card distribution: ", self.rand_card_dist)
        
        

    def draw_from_discard_pile(self):
        self.deck_size -= 1
        if self.deck_size <= 2:
            self.state = "end_game"
        if self.main_player_index == self.turn_index:
            self.main_player_hand.add(self.top_card_discard_pile)
            self.opponent_category_dist[6] += 1
            #self.action = Action("Draw from discard pile", self.top_card_discard_pile, self.main_player.name)
            #If the card from the discard pile is a phantom card, we may not need to go further down the tree, because we will always rather draw from the random deck
        else: 
            #TODO Adjust "probability score" of opponent, because it did draw from the discard pile
            self.opponent_category_dist = self.oracle.update_category_dist(self.opponent_known_cards, self.opponent_category_dist, True, self.top_card_discard_pile)
            self.opponent_known_cards.append(self.top_card_discard_pile)
            #self.action = Action("Draw from discard pile", self.top_card_discard_pile, "opponent")
            self.probability = self.probability/2
            if self.top_card_discard_pile.isPhantom:
                self.state = "end_game"
        
        self.discard_pile.pop()
        if self.state != "end_game":
            self.state = "discard"

        
    def draw_card(self):
        self.deck_size -= 1
        if self.deck_size <= 2:
            self.state = "end_game"
        new_card = Card("", "")
        new_card.make_phantom_card(self.rand_card_dist)
        
        if self.main_player_index == self.turn_index:
            #Adding a random card to hand
            
            self.main_player_hand.add(new_card)
            #self.action = Action("Draw from deck", new_card, self.main_player.name)
        
        #TODO Adjust "probability score" of opponent, because it did not draw from the discard pile
        else:
            #print("Opponent drew from deck")
            #self.action = Action("Draw from deck", new_card, "opponent")
            self.probability = self.probability/2

        
        self.state = "discard"
    
    def discard_from_hand(self, card=None):
        if self.main_player_index == self.turn_index and card is not None:
            
            self.main_player_hand.cards.remove(card)
            #self.action = Action("Discard", card, self.main_player.name)

            #if self.main_player_expected_utility <= 10:
            #    self.state = "knock"

        else:
            card = Card("", "")
            card.make_phantom_card(self.rand_card_dist)
            #self.action = Action("Discard", card, "opponent")

        self.discard_pile.append(card)
        self.top_card_discard_pile = card
        
        self.state = "draw"
        self.turn_index = (self.turn_index + 1) % 2
        if self.turn_index == 0:
            self.round_number += 1

    def knock(self):
        self.state = "end_game"
    
    def print_state(self):
        print("--------------------")
        print("State: ", self.state)
        print("Round number: ", self.round_number)
        #print("Action done this turn: ", self.action)
        print("Main player's hand: ", self.main_player_hand)
        print("Main player's deadwood: ", self.main_player_deadwood)
        print("Main player's expected utility: ", self.main_player_expected_utility)
        print("Discard pile: ", self.discard_pile)
        #print("Top card of discard pile: ", self.top_card_discard_pile)
        print("Known cards: ", self.opponent_known_cards)
        #print("Opponent category distribution: ", self.opponent_category_dist)
        #print("Random card distribution: ", self.rand_card_dist)
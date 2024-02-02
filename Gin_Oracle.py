import random
from Gin_Rummy import Gin_Rummy
from Hand import Hand
from Deck import Deck
from copy import deepcopy

from Player import Player
class Gin_Oracle:
    def __init__(self):
        #Making for smaller deck for now
        self.close_valued_cards = {
            '5': ['6', '7', '8'],
            '6': ['5', '7', '8', '9'],
            '7': ['5', '6', '8', '9', '10'],
            '8': ['5', '6', '7', '9', 'Jack', 'Queen'],
            '9': ['6', '7', '8', '10', 'Jack', 'Queen', 'King'],
            '10': ['7', '8', '9', 'Jack', 'Queen', 'King'],
            'Jack': ['8', '9', '10', 'Queen', 'King'],
            'Queen': ['9', '10', 'Jack', 'King'],
            'King': ['10', 'Jack', 'Queen']
        }
        self.low_valued_cards = ['5', '6', '7']
        self.deck = Deck()
        self.deck.make_smaller_deck()
        pass

    #TODO - Implement get expected value from hand with phantom cards
    def get_expected_utility(self, hand):

        phantom_cards = []
        determenistic_cards_hand = Hand()

        for c in hand.cards:
            if c.isPhantom:
                phantom_cards.append(c)
            else:
                determenistic_cards_hand.add(c)
        
        expected_deadwood = self.get_avg_deadwood(phantom_cards, hand.deadwood, determenistic_cards_hand)
        pc_utility = expected_deadwood - hand.deadwood
        #print("Determenistic deadwood: ", hand.deadwood)
        #print("Phantom card utility: ", pc_utility)
        #print("Expected utility: ", expected_deadwood)
        return expected_deadwood
    
    
    def get_avg_deadwood(self, phantom_cards, determenistic_deadwood, hand):
        if len(phantom_cards) == 0:
            return determenistic_deadwood

        else:
            deck = Deck()
            deck.make_smaller_deck()
            pc_utility = 0
            for i in range(len(phantom_cards)):
                for j in range(len(deck)):

                    if phantom_cards[i].phantom_values[j] == 0:
                        continue

                    temp_hand = deepcopy(hand)
                    temp_hand.cards.append(deck[j])
                    #print("Temp hand: ", temp_hand)
                    pc_utility += (phantom_cards[i].phantom_values[j] * temp_hand.get_hand_score())
                     
        return pc_utility/len(phantom_cards)
    
    #I do not think this is needed
    def update_random_card_dist(self, player_hand, known_cards, discard_pile):

        random_card_dist = [0] * len(self.deck)
        cards_available_counter = 0
        
        for i in range(len(self.deck)):
            if self.deck[i] in  player_hand or self.deck[i] in known_cards or self.deck[i] in discard_pile:
                random_card_dist[i] = 0
            else:
                random_card_dist[i] = 1
                cards_available_counter += 1

        random_card_dist = [x / cards_available_counter for x in random_card_dist]
        return random_card_dist
        

    def update_category_dist(self, opponent_known_cards, category_dist, drew_from_dicard_pile, card_drawn=None):
        #Just a simple implementation for now, theese are temporary
        #Category #0 - 3 or 4 of a kind
        #Category #1 - 3 or more cards in sequence in same suit
        #Category #2 - Low deadwood
        #Category #3 - Lowering deadwood with low value cards - possibly close to knocking
        #Category #4 - Gin
        #Category #5 - Undercut
        #Category #6 - Info about opponent (The main player)

        if drew_from_dicard_pile:
            if card_drawn.isPhantom:
                return category_dist
            if len(opponent_known_cards) > 0:
                #Check if know cards can make a meld with the card drawn
                if len(opponent_known_cards) > 2:
                    hasMeld = self.check_for_meld_equal_cards(opponent_known_cards)
                    if hasMeld:
                        category_dist[0] = 10
                        category_dist[2] += 2
                        category_dist[4] += 1

                    #hasSequence = self.check_for_sequence(opponent_known_cards)

                for c in opponent_known_cards:
                    #print("Card drawn: ", card_drawn.value, " Card in hand: ", c.value)
                    if c.value == card_drawn.value:
                        category_dist[0] += 1
                        category_dist[2] += 0.2
                        category_dist[4] += 0.1     
                    if c.value in self.close_valued_cards[card_drawn.value]:
                        category_dist[1] += 1
                        category_dist[2] += 0.2
                        category_dist[4] += 0.1

            if card_drawn.value in self.low_valued_cards:
                category_dist[2] += 0.2
                category_dist[3] += 0.2
                category_dist[4] += 0.1
            
            category_dist[5] += 1
        
        return category_dist

    def check_for_meld_equal_cards(self, hand):
        #Check for equal cards
        for i in range(len(hand)):
            equal_cards = [hand[i]]
            for j in range(i+1, len(hand)):
                if hand[i].value == hand[j].value:
                    equal_cards.append(hand[j])
                else:
                    break

            if len(equal_cards) >= 3:
                return True
        
        return False

        return category_dist
    
    def check_for_sequence(self, hand):
        #TODO - implement
        return False
    
    def create_random_game(self):
        player1 = Player("Player 1")
        player2 = Player("Player 2")
        game = Gin_Rummy(player1, player2)
        game.start_new_game()

        rand_round_number = random.randint(1, 10)
        rand_discard_number = random.randint(0, rand_round_number) - 1
        rest_number = rand_round_number - rand_discard_number

        for i in range(rand_discard_number):
            game.discard_pile.append(game.deck.deal())
        
        known_cards = []
        for i in range(rest_number):
            known_cards.append(game.deck.deal())
        
        stages = ["draw", "discard"]
        random_stage = stages[(random.randint(0, 1))]

        if random_stage == "discard":
            game.players[game.turn_index].hand.add(game.deck.deal())

        return game, known_cards, random_stage

    

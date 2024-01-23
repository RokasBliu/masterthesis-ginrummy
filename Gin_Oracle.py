from Hand import Hand
from Deck import Deck
from Card import Card
from copy import deepcopy, copy
class Gin_Oracle:
    def __init__(self):
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
        
        determenistic_deadwood = determenistic_cards_hand.get_hand_score()
        expected_deadwood = self.get_avg_deadwood(phantom_cards, determenistic_deadwood, determenistic_cards_hand)
        pc_utility = expected_deadwood - determenistic_deadwood
        print("Determenistic deadwood: ", determenistic_deadwood)
        print("Phantom card utility: ", pc_utility)
        print("Expected utility: ", expected_deadwood)
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
                     
        return pc_utility
from LookupTable import LookupTable

class Hand(object):
    def __init__(self):
        self.cards = []
        self.melds = []
        self.deadwood = 0
        self.rank_converter = {'Ace': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
                   'Jack': 11, 'Queen': 12, 'King': 13}
        self.card_values = {'Ace': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 
               'Jack': 10, 'Queen': 10, 'King': 10}
        # Sort instantly when the hand is created
        self.sort_by_rank()
    
    def __repr__(self):
        return f"{self.cards}"
    
    def add(self, card):
        self.cards.append(card)

    def swap(self, i, j, list):
        temp = list[i]
        list[i] = list[j]
        list[j] = temp
    
    def sort_by_rank(self):
        for i in range(len(self.cards)):
            for j in range(i, len(self.cards)):
                if self.get_card_rank(self.cards[i].value) > self.get_card_rank(self.cards[j].value):
                    self.swap(i, j, self.cards)
        
        return self.cards

    def sort_by_suit(self):
        self.cards.sort(key=lambda card: card.suit)
    
    def get_card_rank(self, card_value):
        return self.rank_converter[card_value]
    
    def check_lookup_table(self, lookup_table, i, j, tuple_values = None, tuple_suits_suits = None):
        #TODO: Implement this, makes the code more readable
        pass
                

            


            
    

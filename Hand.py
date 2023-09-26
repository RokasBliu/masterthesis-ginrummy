class Hand(object):
    def __init__(self):
        self.cards = []
        self.melds = []
        self.deadwood = 0
        self.rank_converter = {'Ace': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
                   'Jack': 11, 'Queen': 12, 'King': 13}
        self.card_values = {'Ace': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 
               'Jack': 10, 'Queen': 10, 'King': 10}
    
    def __repr__(self):
        return f"{self.cards}"
    
    def add(self, card):
        self.cards.append(card)

    def swap(self, i, j, list):
        temp = list[i]
        list[i] = list[j]
        list[j] = temp
    
    def flatten(self, list):
        return [item for sublist in list for item in sublist]
    
    def sort_by_rank(self):
        for i in range(len(self.cards)):
            for j in range(i, len(self.cards)):
                if self.get_card_rank(self.cards[i].value) > self.get_card_rank(self.cards[j].value):
                    self.swap(i, j, self.cards)
        
        return self.cards

    def get_card_rank(self, card_value):
        return self.rank_converter[card_value]
    
    ##TODO: Optimaliser denne
    def get_hand_score(self):
        self.deadwood = 0
        self.melds = []
        self.sort_by_rank()
        for i in range(len(self.cards)):
            equal_cards = [self.cards[i]]
            for j in range(i+1, len(self.cards)):
                if self.cards[i].value == self.cards[j].value:
                    equal_cards.append(self.cards[j])
                else:
                    break
            if len(equal_cards) >= 3:
                self.melds.append(equal_cards)
        
        if len(self.melds) == 0:
            for c in self.cards:
                self.deadwood += self.card_values[c.value]
        else:
            for c in self.cards:
                if c not in self.flatten(self.melds):
                    self.deadwood += self.card_values[c.value]

        print("Cards", self.cards)
        print("Melds", self.melds)
        print(self.deadwood)
        
        return self.deadwood
                


            
    

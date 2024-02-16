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

    ##TODO: Optimaliser denne
    def get_hand_score(self):
        self.deadwood = 0
        self.melds = []
        self.meld_id_counter = 0

        #Reset meld_ids
        for c in self.cards:
            c.meld_ids = []

        self.sort_by_rank()

        #Check for equal cards
        #TODO: må lagre alle permutations av melds
        for i in range(len(self.cards)):
            equal_cards = [self.cards[i]]
            for j in range(i+1, len(self.cards)):
                if self.cards[i].value == self.cards[j].value:
                    equal_cards.append(self.cards[j])
                else:
                    break
            if len(equal_cards) >= 3:
                if len(equal_cards) == 3:
                    self.melds.append(equal_cards)
                    for c in equal_cards:
                        c.meld_ids.append(self.meld_id_counter)
                    self.meld_id_counter += 1

                elif len(equal_cards) == 4:
                    for c in equal_cards:
                        c.meld_ids.append(self.meld_id_counter)   
                    self.melds.append(equal_cards)
                    self.meld_id_counter += 1

                    for c in equal_cards[1:]:
                        c.meld_ids.append(self.meld_id_counter)
                    self.melds.append(equal_cards[1:])
                    self.meld_id_counter += 1

                    temp = equal_cards[:1] + equal_cards[2:]
                    for c in temp:
                        c.meld_ids.append(self.meld_id_counter)
                    self.melds.append(temp)
                    self.meld_id_counter += 1

                    temp = equal_cards[:2] + equal_cards[3:]
                    for c in temp:
                        c.meld_ids.append(self.meld_id_counter)
                    self.melds.append(temp)
                    self.meld_id_counter += 1            

                    

        #Check for straights
        ##TODO: Sjekk om denne faktisk funker
        ##Etter litt testing ser det ut som den funker
        for i in range(len(self.cards)):
            k = i
            straight_suits = [self.cards[i]]
            straight_values = [self.rank_converter[self.cards[i].value]]
            for j in range(i+1, len(self.cards)):
                if self.rank_converter[self.cards[k].value] == self.rank_converter[self.cards[j].value] - 1:
                    if self.cards[k].suit == self.cards[j].suit:
                        straight_suits.append(self.cards[j])
                        straight_values.append(self.rank_converter[self.cards[j].value])
                        k = j
                        if len(straight_suits) >= 3:
                            for c in straight_suits:
                                c.meld_ids.append(self.meld_id_counter)

                            self.melds.append(straight_suits[:])
                            self.meld_id_counter += 1
                            
                                

                elif self.rank_converter[self.cards[k].value] == self.rank_converter[self.cards[j].value]:
                    continue
                else:
                    break

        best_meld = self.find_best_meld()            
        
        if best_meld == None:
            for c in self.cards:
                self.deadwood += self.card_values[c.value]

        else:
            for c in self.cards:
                if c not in best_meld:
                    self.deadwood += self.card_values[c.value]

        #print("Cards", self.cards)
        #print melds in a nice way
        #for m in self.melds:
            #print("Meld: ", m)
        #print("------------------")
        #print("Best meld", best_meld)
        #print("Deadwood:", self.deadwood)
        
        return self.deadwood
                

            


            
    

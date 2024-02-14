from LookupTable import LookupTable
class Hand(object):
    def __init__(self):
        self.cards = []
        self.melds = []
        self.meld_id_counter = 0
        self.deadwood = 0
        self.rank_converter = {'Ace': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
                   'Jack': 11, 'Queen': 12, 'King': 13}
        self.card_values = {'Ace': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 
               'Jack': 10, 'Queen': 10, 'King': 10}
        self.lookup_table = LookupTable()
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
    
    def flatten(self, list):
        return [item for sublist in list for item in sublist]
    
    def sort_by_rank(self):
        for i in range(len(self.cards)):
            for j in range(i, len(self.cards)):
                if self.get_card_rank(self.cards[i].value) > self.get_card_rank(self.cards[j].value):
                    self.swap(i, j, self.cards)
        
        return self.cards

    def sort_by_suit(self):
        self.cards.sort(key=lambda card: card.suit)

    #We need to sort by suits, and get both the suits and the values in a tuple
    def get_hand_suits_tuples(self):
        hand_sorted_suit = sorted(self.cards, key=lambda card: card.suit)
        tuple_suits_suits = tuple()
        tuple_values = tuple()

        for card in hand_sorted_suit:
            tuple_suits_suits += (card.suit,)
            tuple_values += (card.value,)

        return tuple_suits_suits, tuple_values
        
    def get_hand_values_tuple(self):
        hand_sorted_values = sorted(self.cards, key=lambda card: self.get_card_rank(card.value))
        tuple_values = tuple()

        for card in hand_sorted_values:
            tuple_values += (card.value,)
        
        return tuple_values
    
    def get_card_rank(self, card_value):
        return self.rank_converter[card_value]
    
    def get_hand_score_optimized(self):
        self.deadwood = 0
        self.melds = []
        self.meld_id_counter = 0

        #Get the tuples, sorted by suits and values
        #The tuple sorted by suits needs both the suits and the values
        tuple_suits_suits, tuple_suits_values = self.get_hand_suits_tuples()
        tuple_values = self.get_hand_values_tuple()

        print("Tuple suits", tuple_suits_suits)
        print("Tuple values", tuple_suits_values)
        print("Tuple values", tuple_values)
        # Check for straights
        self.sort_by_suit()
        i = 0
        j = 3

        has_straight_three = False
        has_straight_four = False
        has_straight_five = False
        has_straight_six = False

        while j <= len(self.cards):
            print("Tuple values", tuple_suits_suits[i:j])
            if self.lookup_table.flush_three.get(tuple_suits_suits[i:j], 0):
                print("Flush three", tuple_suits_suits[i:j])
                if self.lookup_table.straight_three.get(tuple_suits_values[i:j], 0):
                    cards_to_add = self.cards[i:j]
                    for c in cards_to_add:
                        c.meld_ids.append(self.meld_id_counter)
                    self.melds.append(self.cards[i:j])
                    self.meld_id_counter += 1
                    has_straight_three = True
            i += 1
            j += 1
        
        if has_straight_three:
            i = 0
            j = 4
            while j <= len(self.cards):
                if self.lookup_table.flush_four.get(tuple_suits_suits[i:j], 0):
                    if self.lookup_table.straight_four.get(tuple_suits_values[i:j], 0):
                        cards_to_add = self.cards[i:j]
                        for c in cards_to_add:
                            c.meld_ids.append(self.meld_id_counter)
                        self.melds.append(self.cards[i:j])
                        self.meld_id_counter += 1
                        has_straight_four = True
                i += 1
                j += 1
        
        if has_straight_four:
            i = 0
            j = 5
            while j <= len(self.cards):
                if self.lookup_table.flush_five.get(tuple_suits_suits[i:j], 0):
                    if self.lookup_table.straight_five.get(tuple_suits_values[i:j], 0):
                        cards_to_add = self.cards[i:j]
                        for c in cards_to_add:
                            c.meld_ids.append(self.meld_id_counter)
                        self.melds.append(self.cards[i:j])
                        self.meld_id_counter += 1
                        has_straight_five = True
                i += 1
                j += 1
        
        if has_straight_five:
            i = 0
            j = 6
            while j <= len(self.cards):
                if self.lookup_table.flush_six.get(tuple_suits_suits[i:j], 0):
                    if self.lookup_table.straight_six.get(tuple_suits_values[i:j], 0):
                        cards_to_add = self.cards[i:j]
                        for c in cards_to_add:
                            c.meld_ids.append(self.meld_id_counter)
                        self.melds.append(self.cards[i:j])
                        self.meld_id_counter += 1
                        has_straight_six = True
                i += 1
                j += 1
        
        if has_straight_six:
            i = 0
            j = 7
            while j <= len(self.cards):
                if self.lookup_table.flush_seven.get(tuple_suits_suits[i:j], 0):
                    if self.lookup_table.straight_seven.get(tuple_suits_values[i:j], 0):
                        cards_to_add = self.cards[i:j]
                        for c in cards_to_add:
                            c.meld_ids.append(self.meld_id_counter)
                        self.melds.append(self.cards[i:j])
                        self.meld_id_counter += 1
                i += 1
                j += 1
        
        # Check for equal cards
        self.sort_by_rank()
        i = 0
        j = 3
        has_three_of_a_kind = False
        while j <= len(self.cards):
            if self.lookup_table.three_of_a_kind.get(tuple_values[i:j]):
                cards_to_add = self.cards[i:j]
                for c in cards_to_add:
                    c.meld_ids.append(self.meld_id_counter)
                self.melds.append(self.cards[i:j])
                self.meld_id_counter += 1
                has_three_of_a_kind = True
            i += 1
            j += 1

        if has_three_of_a_kind:
            i = 0
            j = 4
            while j <= len(self.cards):
                if self.lookup_table.four_of_a_kind.get(tuple_values[i:j]):
                    cards_to_add = self.cards[i:j]
                    for c in cards_to_add:
                        c.meld_ids.append(self.meld_id_counter)
                    self.melds.append(self.cards[i:j])
                    self.meld_id_counter += 1
                i += 1
                j += 1
        
        best_meld = self.find_best_meld()            
        
        if best_meld == None:
            for c in self.cards:
                self.deadwood += self.card_values[c.value]

        else:
            for c in self.cards:
                if c not in best_meld:
                    self.deadwood += self.card_values[c.value]

        print("------------------")
        print("Cards", self.cards)
        print("melds", self.melds)
        print("Best meld", best_meld)
        print("Deadwood:", self.deadwood)
        return self.deadwood
    
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
                
    def find_best_meld(self):

        meld_conflict = False
        if len(self.melds) == 0:
            return None
        
        if len(self.melds) == 1:
            return self.melds[0]

        for c in self.flatten(self.melds):
            if len(c.meld_ids) > 1:
                meld_conflict = True
                #print("Meld conflict")
                break

        if meld_conflict == False:
            return self.flatten(self.melds)        
        else:

            best_meld = self.melds[0]
            best_meld_deadwood = 0
            for c in self.cards:
                if c not in best_meld:
                    best_meld_deadwood += self.card_values[c.value]

            #Check if melds can be combined
            for i in range(len(self.melds)):
                for j in range(i+1, len(self.melds)):
                    can_combine = True
                    ##Check for conflict
                    for c in self.melds[i]:
                        if c in self.melds[j]:
                            can_combine = False
                            break
                    
                    if can_combine == True:
                        self.melds.append(self.melds[i] + self.melds[j])
                    
                            


            for i in range(len(self.melds)):

                meld_i_deadwood = 0

                #print("------------------")
                #print("Meld", self.melds[i])

                for c in self.cards:
                    if c not in self.melds[i]:
                        meld_i_deadwood += self.card_values[c.value]

                #print("Meld deadwood", meld_i_deadwood)
                #print("Best meld deadwood", best_meld_deadwood)
                #print("------------------")
                if meld_i_deadwood < best_meld_deadwood:
                    best_meld = self.melds[i]
                    best_meld_deadwood = meld_i_deadwood


        return best_meld

            


            
    

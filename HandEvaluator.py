from Hand import Hand
from LookupTable import LookupTable
class HandEvaluator:
    def __init__(self):
        self.lookup_table = LookupTable()
        self.meld_id_counter = 0
        self.melds = []

    #We need to sort by suits, and get both the suits and the values in a tuple
    def get_hand_suits_tuples(self, hand: Hand):
        hand_sorted_suit = sorted(hand.cards, key=lambda card: card.suit)
        tuple_suits_suits = tuple()
        tuple_values = tuple()

        for card in hand_sorted_suit:
            tuple_suits_suits += (card.suit,)
            tuple_values += (card.value,)

        return tuple_suits_suits, tuple_values
        
    def get_hand_values_tuple(self, hand: Hand):
        hand_sorted_values = sorted(hand.cards, key=lambda card: hand.get_card_rank(card.value))
        tuple_values = tuple()

        for card in hand_sorted_values:
            tuple_values += (card.value,)
        
        return tuple_values

    def flatten(self, list):
        return [item for sublist in list for item in sublist]
    
    def get_hand_score(self, hand: Hand, wants_melds_returned = False, wants_best_meld = False):
        hand.deadwood = 0
        self.melds = []
        self.meld_id_counter = 0

        #Get the tuples, sorted by suits and values
        #The tuple sorted by suits needs both the suits and the values
        tuple_suits_suits, tuple_suits_values = self.get_hand_suits_tuples(hand)
        tuple_values = self.get_hand_values_tuple(hand)

        # Check for straights
        hand.sort_by_suit()
        i = 0
        j = 3

        has_straight_three = False
        has_straight_four = False
        has_straight_five = False
        has_straight_six = False

        while j <= len(hand.cards):
            if self.lookup_table.flush_three.get(tuple_suits_suits[i:j], 0):
                if self.lookup_table.straight_three.get(tuple_suits_values[i:j], 0):
                    cards_to_add = hand.cards[i:j]
                    for c  in cards_to_add:
                        c.meld_ids.append(self.meld_id_counter)
                    self.melds.append(hand.cards[i:j])
                    self.meld_id_counter += 1
                    has_straight_three = True
            i += 1
            j += 1
        
        if has_straight_three:
            i = 0
            j = 4
            while j <= len(hand.cards):
                if self.lookup_table.flush_four.get(tuple_suits_suits[i:j], 0):
                    if self.lookup_table.straight_four.get(tuple_suits_values[i:j], 0):
                        cards_to_add = hand.cards[i:j]
                        for c in cards_to_add:
                            c.meld_ids.append(self.meld_id_counter)
                        self.melds.append(hand.cards[i:j])
                        self.meld_id_counter += 1
                        has_straight_four = True
                i += 1
                j += 1
        
        #TODO: Implement this
        if has_straight_four:
            i = 0
            j = 5
            while j <= len(hand.cards):
                if self.lookup_table.flush_five.get(tuple_suits_suits[i:j], 0):
                    if self.lookup_table.straight_five.get(tuple_suits_values[i:j], 0):
                        cards_to_add = hand.cards[i:j]
                        for c in cards_to_add:
                            c.meld_ids.append(self.meld_id_counter)
                        self.melds.append(hand.cards[i:j])
                        self.meld_id_counter += 1
                        has_straight_five = True
                i += 1
                j += 1
        
        if has_straight_five:
            i = 0
            j = 6
            while j <= len(hand.cards):
                if self.lookup_table.flush_six.get(tuple_suits_suits[i:j], 0):
                    if self.lookup_table.straight_six.get(tuple_suits_values[i:j], 0):
                        cards_to_add = hand.cards[i:j]
                        for c in cards_to_add:
                            c.meld_ids.append(self.meld_id_counter)
                        self.melds.append(hand.cards[i:j])
                        self.meld_id_counter += 1
                        has_straight_six = True
                i += 1
                j += 1
        
        if has_straight_six:
            i = 0
            j = 7
            while j <= len(hand.cards):
                if self.lookup_table.flush_seven.get(tuple_suits_suits[i:j], 0):
                    if self.lookup_table.straight_seven.get(tuple_suits_values[i:j], 0):
                        cards_to_add = hand.cards[i:j]
                        for c in cards_to_add:
                            c.meld_ids.append(self.meld_id_counter)
                        self.melds.append(hand.cards[i:j])
                        self.meld_id_counter += 1
                i += 1
                j += 1
        
        # Check for equal cards
        hand.sort_by_rank()
        i = 0
        j = 3
        has_three_of_a_kind = False
        while j <= len(hand.cards):
            if self.lookup_table.three_of_a_kind.get(tuple_values[i:j]):
                cards_to_add = hand.cards[i:j]
                for c in cards_to_add:
                    c.meld_ids.append(self.meld_id_counter)
                self.melds.append(hand.cards[i:j])
                self.meld_id_counter += 1
                has_three_of_a_kind = True
            i += 1
            j += 1

        if has_three_of_a_kind:
            i = 0
            j = 4
            while j <= len(hand.cards):
                if self.lookup_table.four_of_a_kind.get(tuple_values[i:j]):
                    cards_to_add = hand.cards[i:j]
                    for c in cards_to_add:
                        c.meld_ids.append(self.meld_id_counter)
                    self.melds.append(hand.cards[i:j])
                    self.meld_id_counter += 1
                i += 1
                j += 1
        
        best_meld = self.find_best_meld(hand)

        if best_meld == None:
            for c in hand.cards:
                hand.deadwood += hand.card_values[c.value]

        else:
            for c in hand.cards:
                if c not in best_meld:
                    hand.deadwood += hand.card_values[c.value]

        if wants_melds_returned:
            return hand.deadwood, self.melds
        
        if wants_best_meld:
            return hand.deadwood, best_meld

        return hand.deadwood
    
    def find_best_meld(self, hand: Hand):

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
            for c in hand.cards:
                if c not in best_meld:
                    best_meld_deadwood += hand.card_values[c.value]

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

                for c in hand.cards:
                    if c not in self.melds[i]:
                        meld_i_deadwood += hand.card_values[c.value]

                #print("Meld deadwood", meld_i_deadwood)
                #print("Best meld deadwood", best_meld_deadwood)
                #print("------------------")
                if meld_i_deadwood < best_meld_deadwood:
                    best_meld = self.melds[i]
                    best_meld_deadwood = meld_i_deadwood

        return best_meld
from Deck import Deck, Card
from Hand import Hand

class Test():
    def test_card_in_two_melds_edgecase(self):
        hand = Hand()

        hand.cards = [Card("Hearts", "5"), 
                        Card("Hearts", "6"), 
                        Card("Hearts", "7"), 
                        Card("Hearts", "8"), 
                        Card("Spades", "8"), 
                        Card("Diamonds", "8"),
                        Card("Hearts", "King")]

        hand.sort_by_rank()
        score = hand.get_hand_score()

        assert score == 10, f"Hand score (deadwood) should be 10, got {score}"

    def test_find_best_meld_edgecase(self):
        hand = Hand()

        hand.cards = [Card("Hearts", "5"), 
                        Card("Hearts", "6"), 
                        Card("Hearts", "7"), 
                        Card("Hearts", "8"), 
                        Card("Spades", "6"), 
                        Card("Diamonds", "6"),
                        Card("Hearts", "King")]

        hand.sort_by_rank()
        score = hand.get_hand_score()

        assert score == 22, f"Hand score (deadwood) should be 22, got {score}"

    def test_find_full_straight(self):
        hand = Hand()

        hand.cards = [Card("Hearts", "5"), 
                        Card("Hearts", "6"), 
                        Card("Hearts", "7"), 
                        Card("Hearts", "8"), 
                        Card("Hearts", "9"), 
                        Card("Hearts", "10"),
                        Card("Hearts", "Jack")]

        hand.sort_by_rank()
        score = hand.get_hand_score()

        assert score == 0, f"Hand score (deadwood) should be 0, got {score}"

    def test_hand_add(self):
        hand = Hand()

        hand.cards = [Card("Hearts", "5"), 
                        Card("Hearts", "6"), 
                        Card("Hearts", "7"), 
                        Card("Hearts", "8"), 
                        Card("Spades", "8"), 
                        Card("Diamonds", "8"),
                        Card("Hearts", "King")]
        
        hand.sort_by_rank()
        score = hand.get_hand_score()

        assert len(hand.cards) == 7, f"Amount of cards in hand should be 7, got {len(hand.cards)}"
        assert score == 10, f"Hand score (deadwood) should be 10, got {score}"

        hand.add(Card("Hearts", "9"))
        score = hand.get_hand_score()

        assert len(hand.cards) == 8, f"Amount of cards in hand should be 8, got {len(hand.cards)}"
        assert score == 19, f"Hand score (deadwood) should be 19, got {score}"

    def test_sort_hand_by_rank(self):
        hand = Hand()

        hand.cards = [Card("Clubs", "King"), 
                        Card("Hearts", "Jack"), 
                        Card("Hearts", "7"), 
                        Card("Hearts", "Queen"), 
                        Card("Spades", "5"), 
                        Card("Diamonds", "8"),
                        Card("Hearts", "8")]

        hand.sort_by_rank()

        assert hand.cards == [Card("Spades", "5"),
                        Card("Hearts", "7"),
                        Card("Diamonds", "8"),
                        Card("Hearts", "8"),
                        Card("Hearts", "Jack"),
                        Card("Hearts", "Queen"),
                        Card("Clubs", "King")], "Hand was not sorted by rank correctly"

    
def main():
    test = Test()

    test.test_card_in_two_melds_edgecase()
    test.test_find_best_meld_edgecase()
    test.test_find_full_straight()
    test.test_hand_add()
    test.test_sort_hand_by_rank()

    print("All tests passed successfully")

if __name__ == "__main__":
    main()


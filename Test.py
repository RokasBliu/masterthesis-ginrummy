
from Card import Card
from Deck import Deck
from Hand import Hand
from Player import Player
from Gin_Rummy import Gin_Rummy
import pytest

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


    def test_deck(self):
        deck = Deck()
        assert len(deck) == 52, "Normal deck size should be 52"

        deck.shuffle()
        assert len(deck) == 52, "Normal deck size after shuffling should still be 52"

        deck.make_smaller_deck()
        assert len(deck) == 36, "Smaller deck (in this implementation) should be of size 36"

        deck.shuffle()
        assert len(deck) == 36, "Smaller deck size after shuffling should still be the same"


    def test_game_start_with_normal_deck(self):
        player1 = Player("Test Player 1")
        player2 = Player("Test Player 2")

        game = Gin_Rummy(player1, player2)
        game.start_new_game(False) # Start game with a normal sized deck

        assert game.players[0].name == "Test Player 1" and game.players[1].name == "Test Player 2", "Player names do not match"
        assert len(game.deck) == 31, f"The deck should have 31 cards left, but has {len(game.deck)}"
        assert len(game.discard_pile) == 1, f"Discard pile should have 1 card, but has {len(game.discard_pile)}"


    def test_game_start_with_small_deck(self):
        player1 = Player("Test Player 1")
        player2 = Player("Test Player 2")

        game = Gin_Rummy(player1, player2)
        game.start_new_game(True) # Start game with a smaller deck

        assert game.players[0].name == "Test Player 1" and game.players[1].name == "Test Player 2", "Player names do not match"
        assert len(game.deck) == 21, f"The deck should have 21 cards left, but has {len(game.deck)}"
        assert len(game.discard_pile) == 1, f"Discard pile should have 1 card, but has {len(game.discard_pile)}"

    
    def test_player_draw_random_and_discard(self, monkeypatch):
        responses = iter(["random", "1", "n"])
        monkeypatch.setattr("builtins.input", lambda inp: next(responses))

        player1 = Player("Test Player 1")
        player2 = Player("Test Player 2")

        game = Gin_Rummy(player1, player2)
        game.start_new_game(True) # Start game with a smaller deck

        assert game.players[0].name == "Test Player 1" and game.players[1].name == "Test Player 2", "Player names do not match"
        assert len(game.deck) == 21, f"The deck should have 21 cards left, but has {len(game.deck)}"
        assert len(game.discard_pile) == 1, f"Discard pile should have 1 card, but has {len(game.discard_pile)}"

        game.draw(game.players[game.turn_index])

        assert len(game.deck) == 20, f"The deck should have 20 cards left, but has {len(game.deck)}"
        assert len(game.discard_pile) == 1, f"Discard pile should have 1 card, but has {len(game.discard_pile)}"
        assert len(game.players[0].hand.cards) == 8, f"Player should have drawn an extra card but has {len(game.players[0].hand.cards)}"

        game.discard(game.players[game.turn_index])

        assert len(game.deck) == 20, f"The deck should have 20 cards left, but has {len(game.deck)}"
        assert len(game.discard_pile) == 2, f"Discard pile should have 2 card, but has {len(game.discard_pile)}"
        assert len(game.players[0].hand.cards) == 7, "Player should have 7 cards in hand"
        assert game.turn_index == 1, "It should be next player's turn now"


    def test_player_draw_discard_and_discard(self, monkeypatch):
        responses = iter(["discard", "1", "n"])
        monkeypatch.setattr("builtins.input", lambda inp: next(responses))

        player1 = Player("Test Player 1")
        player2 = Player("Test Player 2")

        game = Gin_Rummy(player1, player2)
        game.start_new_game(True) # Start game with a smaller deck

        assert game.players[0].name == "Test Player 1" and game.players[1].name == "Test Player 2", "Player names do not match"
        assert len(game.deck) == 21, f"The deck should have 21 cards left, but has {len(game.deck)}"
        assert len(game.discard_pile) == 1, f"Discard pile should have 1 card, but has {len(game.discard_pile)}"

        game.draw(game.players[game.turn_index])

        assert len(game.deck) == 21, f"The deck should have 21 cards left, but has {len(game.deck)}"
        assert len(game.discard_pile) == 0, f"Discard pile should have 0 card, but has {len(game.discard_pile)}"
        assert len(game.players[0].hand.cards) == 8, f"Player should have drawn an extra card but has {len(game.players[0].hand.cards)}"

        game.discard(game.players[game.turn_index])

        assert len(game.deck) == 21, f"The deck should have 21 cards left, but has {len(game.deck)}"
        assert len(game.discard_pile) == 1, f"Discard pile should have 2 card, but has {len(game.discard_pile)}"
        assert len(game.players[0].hand.cards) == 7, "Player should have 7 cards in hand"
        assert game.turn_index == 1, "It should be next player's turn now"


    def test_gameflow(self, monkeypatch):
        responses = iter(["discard", "1", "discard", "2", "discard", "1", "y"])
        monkeypatch.setattr("builtins.input", lambda inp: next(responses))

        player1 = Player("Test Player 1")
        player2 = Player("Test Player 2")

        game = Gin_Rummy(player1, player2)
        game.start_new_game(False)

        game.players[0].hand.cards = [Card("Spades", "5"),
                        Card("Hearts", "5"),
                        Card("Diamonds", "8"),
                        Card("Hearts", "8"),
                        Card("Spades", "8"),
                        Card("Hearts", "9"),
                        Card("Hearts", "10"),
                        Card("Hearts", "Jack"),
                        Card("Hearts", "Queen"),
                        Card("Hearts", "King")]

        game.players[1].hand.cards = [Card("Clubs", "8"),
                        Card("Diamonds", "9"),
                        Card("Spades", "10"),
                        Card("Diamonds", "10"),
                        Card("Clubs", "Jack"),
                        Card("Hearts", "Jack"),
                        Card("Hearts", "Queen"),
                        Card("Spades", "Queen"),
                        Card("Clubs", "King"),
                        Card("Diamonds", "King"),]

        game.discard_pile = [Card("Hearts", "7")]

        game.game_flow()

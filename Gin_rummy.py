from  Deck import Deck
from Player import Player
from Hand import Hand
class Gin_rummy(object):
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.turn_index = 0 # 0 for player1, 1 for player2

        self.decline_round = True # the first round

        self.drawing_from_discard = False
        self.game_over = True
        self.strike_one = False
        self.short_of_card = False
        self.round_number = 0
        self.deck = []
        self.discard_pile = []


    def start_new_game(self):
        if self.game_over:
            self.deck = Deck()
            self.deck.make_smaller_deck()
            self.deck.shuffle()
            self.game_over = False
            self.strike_one = False
            
            self.players[0].player_draw = True
            self.players[1].player_draw = False

            for p in self.players:
                p.score = 0
                p.hand = Hand()
            
            self.round_number = 0
            self.deal()
            self.discard_pile.append(self.deck.deal())
        

    def deal(self):
        for i in range(7):
            for p in self.players:
                p.hand.add(self.deck.deal())

    def draw(self, player):
        answering = False
        while answering == False:
            print("Your hand: ", player.hand.sort_by_rank())
            print("Top of discard pile: ", self.discard_pile[-1])
            answer = input("Draw random or from discard?")

            answering = answer.lower() == "random" or answer.lower() == "discard"
        
        if answer.lower() == "random":
            player.hand.add(self.deck.deal())
            self.drawing_from_discard = False
            print("You drew: ", player.hand.cards[-1])
        else:
            player.hand.add(self.discard_pile.pop())
            self.drawing_from_discard = True

    def discard(self, player):
        print("Your hand: ", player.hand.sort_by_rank())
        answer = input("Which card do you want to discard? (1-11)")
        card = player.hand.cards[int(answer)-1]
        player.hand.cards.remove(card)
        self.discard_pile.append(card)
        self.drawing_from_discard = False

        if player.hand.get_hand_score() <= 10:
            player.player_knock = True
            knock_answer = input("Do you want to knock? (y/n)")

            if knock_answer.lower() == "y":
                self.end_round(player)
            else:
                player.player_knock = False
                player.player_discard = False
                player.player_draw = True

        self.turn_index = (self.turn_index + 1) % 2


    def end_round(self, player):
        self.round_number += 1
        self.decline_round = False
        self.game_over = True
        self.strike_one = False
        self.short_of_card = False

        if player.hand.deadwood == 0:
            player.score += 25
        else:
            player.score += player.hand.deadwood

        if player.score >= 100:
            self.game_over = True
            print(f"{player.name} won the game!")
        else:
            self.game_over = False
            self.strike_one = False
            self.short_of_card = False

            for p in self.players:
                p.hand = Hand()
                p.player_draw = False
                p.player_discard = False
                p.player_knock = False

            self.deck = Deck()
            self.deck.make_smaller_deck()
            self.deck.shuffle()
            self.deal()
            self.discard_pile.append(self.deck.deal())

    def game_flow(self):
        self.start_new_game()
        print("Game started")
        while self.game_over == False:
            print("Round number: ", self.round_number)
            print(self.players[self.turn_index].name, "'s turn")
            self.draw(self.players[self.turn_index])
            self.discard(self.players[self.turn_index])
            print("Next turn")

        


def main():
        
    player1 = Player("Player 1")
    player2 = Player("Player 2")

    game = Gin_rummy(player1, player2)
    game.game_flow()

if __name__ == "__main__":
    main()
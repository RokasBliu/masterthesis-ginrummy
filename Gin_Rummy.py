from Deck import Deck
from Player import Player
from Hand import Hand
import threading
import pygame

class Gin_Rummy(object):
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

        self.GIN_POINTS = 25
        self.UNDERCUT_POINTS = 10
        self.WINNING_SCORE = 100

        self.NORMAL_NUM_CARDS_PER_HAND = 10
        self.SMALLER_NUM_CARDS_PER_HAND = 7

        self.is_smaller_deck = False

    def start_new_game(self, with_smaller_deck=True):
        self.is_smaller_deck = with_smaller_deck
        if self.game_over:
            self.deck = Deck()
            if with_smaller_deck:
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
            self.deal(with_smaller_deck)
            self.discard_pile.append(self.deck.deal())
        

    def deal(self, with_smaller_deck=True):
        num_cards = self.NORMAL_NUM_CARDS_PER_HAND
        if with_smaller_deck:
            num_cards = self.SMALLER_NUM_CARDS_PER_HAND
        for i in range(num_cards):
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
        check_if_int = False
        while check_if_int == False:
            answer = input(f"Which card do you want to discard? (1-{self.SMALLER_NUM_CARDS_PER_HAND + 1 if self.is_smaller_deck else self.NORMAL_NUM_CARDS_PER_HAND + 1})")
            check_if_int = True
            try:
                int(answer)
            except ValueError:
                check_if_int = False

        
        card = player.hand.cards[int(answer)-1]
        player.hand.cards.remove(card)
        self.discard_pile.append(card)
        self.drawing_from_discard = False

        if player.hand.get_hand_score() <= 10:
            player.player_knock = True
            knock_answer = input("Do you want to knock? (y/n)")

            if knock_answer.lower() == "y":
                self.knock(player)
            else:
                player.player_knock = False
                player.player_discard = False
                player.player_draw = True

        self.turn_index = (self.turn_index + 1) % 2
        if self.turn_index == 0:
            self.round_number += 1


    def knock(self, player):
        self.round_number += 1
        self.decline_round = False
        self.game_over = True
        self.strike_one = False
        self.short_of_card = False
        other_player = self.players[(self.turn_index + 1) % 2]

        print("------------------")
        print("Knocking player's hand score: ", player.hand.deadwood)
        print("Other player's hand score: ", other_player.hand.deadwood)
        print("------------------")

        if player.hand.deadwood < other_player.hand.deadwood:
            player.score += other_player.hand.deadwood - player.hand.deadwood
        else: # player.hand.deadwood > other_player.hand.deadwood
            other_player.score += player.hand.deadwood - other_player.hand.deadwood + self.UNDERCUT_POINTS

        if player.hand.deadwood == 0:
            player.score += self.GIN_POINTS



        print("Player 1's score: ", self.players[0].score)
        print("Player 2's score: ", self.players[1].score)

        if player.score >= self.WINNING_SCORE:
            self.game_over = True
            print(f"{player.name} won the game!")
        else:
            self.game_over = False
            self.strike_one = False
            self.short_of_card = False

            self.start_new_round()

    def start_new_round(self):
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
        self.start_new_game(True)
        print("------------------")
        print("Game started")
        print("------------------")

        while self.game_over == False:
            # self.key = None
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         self.game_over = True
            #     if event.type == pygame.KEYDOWN:
            #         key = event.key

            print("Round number: ", self.round_number)
            print(self.players[self.turn_index].name, "'s turn")
            self.draw(self.players[self.turn_index])
            self.discard(self.players[self.turn_index])

            # Check if the deck has only 2 cards left, in which case, the game ends in a draw
            if len(self.deck) <= 2:
                self.game_over = False
                self.start_new_round()

            print("Next turn")

def pygame_display(game):
    pygame.init()
    bounds = (1280, 600)
    window = pygame.display.set_mode(bounds, pygame.RESIZABLE)
    pygame.display.set_caption("Gin Rummy boiiiiiiiiiiiiiiiii")
    clock = pygame.time.Clock()
    FPS = 12

    def display_cards(game, window):
        # Define some useful variables
        window_width, window_height = window.get_size()
        screen_width, screen_height = pygame.display.get_desktop_sizes()[0]
        padding = 2

        # Load card back and use it to calculate the new image widths and heights
        common_denomitator = (screen_width * screen_height) / (window_width * window_height)
        card_back = pygame.image.load('images/back.svg')
        card_image_width, card_image_height = card_back.get_size()
        resized_card_width = card_image_width * 0.75 / common_denomitator
        resized_card_height = card_image_height * 0.75 / common_denomitator
        resized_card_back = pygame.transform.scale(card_back, (int(resized_card_width), int(resized_card_height)))

        # Display deck
        window.blit(resized_card_back, ((window_width - resized_card_width) / 2, (window_height - resized_card_height) / 2))

        # Display discard pile
        discard_pile_card = pygame.image.load('images/blank_card.svg')
        if game.discard_pile:
            discard_pile_card = game.discard_pile[-1].image
            discard_pile_card = pygame.transform.scale(discard_pile_card, (int(resized_card_width), int(resized_card_height)))
        window.blit(discard_pile_card, ((window_width - resized_card_width) / 2 - resized_card_width - padding, (window_height - resized_card_height) / 2))

        # Display cards in hand
        player_i = 1
        for player in game.players:
            card_i = 0
            for card in player.hand.cards:
                image = card.image
                # If card isHidden, we want to not show it
                if card.isHidden:
                    image = card_back
                # Transform card's size
                image = pygame.transform.scale(image, (int(resized_card_width), int(resized_card_height)))
                # Render card on screen
                window.blit(image, ((resized_card_width + padding) * card_i, (window_height - resized_card_height)*player_i))
                card_i += 1
            player_i -= 1    

    def display_loop(game, window):
        while True:
            # Handle interrupts, window resizes and "quit" events
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                    if event.type == pygame.VIDEORESIZE:
                        window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            except KeyboardInterrupt:
                break

            # Rendering
            window.fill((30, 92, 58))
            display_cards(game, window)
            pygame.display.update()
            clock.tick(FPS)
    
    display_loop(game, window)
    pygame.quit()

def game_thread(game):
    game.game_flow()

def main():
    player1 = Player("Player 1")
    player2 = Player("Player 2")

    game = Gin_Rummy(player1, player2)

    # Running game logic on a seperate daemon thread
    thread = threading.Thread(target=game_thread, args=(game, ), daemon=True)
    thread.start()

    # This main thread will be running the display
    pygame_display(game)
            

if __name__ == "__main__":
    main()
from Deck import Deck
from Player import Player
from Hand import Hand
from queue import Queue
import threading
import pygame
import sys

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

    def draw(self, player, in_q):
        answering = False
        while answering == False:
            print("Your hand: ", player.hand.sort_by_rank())
            print("Top of discard pile: ", self.discard_pile[-1])
            # answer = input("Draw random or from discard?")
            # answering = answer.lower() == "random" or answer.lower() == "discard"
            answer = in_q.get()
            answering = answer.lower() == "random" or answer.lower() == "discard"
        
        if answer.lower() == "random":
            player.hand.add(self.deck.deal())
            self.drawing_from_discard = False
            print("You drew: ", player.hand.cards[-1])
        else:
            player.hand.add(self.discard_pile.pop())
            self.drawing_from_discard = True

    def discard(self, player, in_q):
        print("Your hand: ", player.hand.sort_by_rank())
        check_if_int = False
        while check_if_int == False:
            # answer = input(f"Which card do you want to discard? (1-{self.SMALLER_NUM_CARDS_PER_HAND + 1 if self.is_smaller_deck else self.NORMAL_NUM_CARDS_PER_HAND + 1})")
            answer = in_q.get()
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
            answering = False
            while answering == False:
                knock_answer = in_q.get()
                answering = knock_answer.lower() == "y" or knock_answer.lower() == "n"

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

    def game_flow(self, in_q):
        self.start_new_game(True)
        print("------------------")
        print("Game started")
        print("------------------")

        while self.game_over == False:
            print("Round number: ", self.round_number)
            print(self.players[self.turn_index].name, "'s turn")
            self.draw(self.players[self.turn_index], in_q)
            self.discard(self.players[self.turn_index], in_q)

            # Check if the deck has only 2 cards left, in which case, the game ends in a draw
            if len(self.deck) <= 2:
                self.game_over = False
                self.start_new_round()

            print("Next turn")

def pygame_display(game, out_q):
    pygame.init()
    bounds = (1280, 600)
    window = pygame.display.set_mode(bounds, pygame.RESIZABLE)
    pygame.display.set_caption("Gin Rummy")
    clock = pygame.time.Clock()
    FPS = 12

    # Init font
    pygame.font.init()
        
    def display_cards(game, window, mouse_click_pos):
        # Define some useful variables
        window_width, window_height = window.get_size()
        screen_width, screen_height = pygame.display.get_desktop_sizes()[0]
        custom_border_width, custom_border_height = (window_width * 0.5, window_height * 0.7)
        custom_window_placement = (window_width/2 - custom_border_width/2, window_height/2 - custom_border_height/2)
        padding = 2

        # Draw window border
        # pygame.draw.line(window, (40, 72, 68), custom_window_placement, (custom_window_placement[0], custom_window_placement[1] + custom_border_height), width=1)
        # pygame.draw.line(window, (40, 72, 68), custom_window_placement, (custom_window_placement[0] + custom_border_width, custom_window_placement[1]), width=1)
        # pygame.draw.line(window, (40, 72, 68), (custom_window_placement[0], custom_window_placement[1] + custom_border_height), (custom_window_placement[0] + custom_border_width, custom_window_placement[1] + custom_border_height), width=1)
        # pygame.draw.line(window, (40, 72, 68), (custom_window_placement[0] + custom_border_width, custom_window_placement[1]), (custom_window_placement[0] + custom_border_width, custom_window_placement[1] + custom_border_height), width=1)

        # Load card back and use it to calculate the new image widths and heights
        #common_denominator = (screen_width * screen_height) / (window_width * window_height)
        card_back = pygame.image.load('images/back.svg')
        card_image_width, card_image_height = card_back.get_size()
        resized_card_height = custom_border_height * 0.25
        resized_card_width = card_image_width * (resized_card_height / card_image_height)
        resized_card_back = pygame.transform.scale(card_back, (int(resized_card_width), int(resized_card_height)))

        # Display deck
        deck_surface = window.blit(resized_card_back, (custom_border_width / 2 + padding + custom_window_placement[0], (custom_border_height - resized_card_height) / 2 + custom_window_placement[1]))

        # Display discard pile
        discard_pile_card = pygame.image.load('images/blank_card.svg')
        if game.discard_pile:
            discard_pile_card = game.discard_pile[-1].image
            discard_pile_card = pygame.transform.scale(discard_pile_card, (int(resized_card_width), int(resized_card_height)))
        discard_pile_surface = window.blit(discard_pile_card, (custom_border_width / 2 - resized_card_width - padding + custom_window_placement[0], (custom_border_height - resized_card_height) / 2 + custom_window_placement[1]))

        # Display cards in hand
        player_card_surfaces = []
        player_i = 1
        for player in game.players:
            card_i = 0
            current_player_card_surfaces = []
            for card in player.hand.cards:
                image = card.image
                # If card isHidden, we want to not show it
                if card.isHidden:
                    image = card_back
                # Transform card's size
                image = pygame.transform.scale(image, (int(resized_card_width), int(resized_card_height)))
                # Render card on screen
                card_surface = window.blit(image,
                 ((resized_card_width + padding) * card_i + (custom_border_width/2 - resized_card_width*(game.SMALLER_NUM_CARDS_PER_HAND / 2 if game.is_smaller_deck else game.NORMAL_NUM_CARDS_PER_HAND / 2) + custom_window_placement[0]),
                 (custom_border_height - resized_card_height) * player_i + custom_window_placement[1]))
                card_i += 1
                current_player_card_surfaces.append(card_surface)
            player_card_surfaces.append(current_player_card_surfaces)
            player_i -= 1

        # Display player text
        my_font = pygame.font.SysFont('Comic Sans MS', 30 // (screen_height // window_height))
        player_1_text = my_font.render('Player 1', False, (0, 0, 0))
        window.blit(player_1_text, (custom_border_width/2 - player_1_text.get_width()/2 + custom_window_placement[0], custom_border_height + custom_window_placement[1] + (window_height - custom_border_height)/8))
        player_2_text = my_font.render('Player 2', False, (0, 0, 0))
        window.blit(player_2_text, (custom_border_width/2 - player_1_text.get_width()/2 + custom_window_placement[0], custom_window_placement[1] - (window_height - custom_border_height)/3))

        # Display player turn
        my_font = pygame.font.SysFont('Comic Sans MS', 20 // (screen_height // window_height))
        player_turn = game.turn_index
        turn_state = "DRAW"
        if len(game.players[player_turn].hand.cards) > game.SMALLER_NUM_CARDS_PER_HAND if game.is_smaller_deck else game.NORMAL_NUM_CARDS_PER_HAND:
            turn_state = "DISCARD"
        turn_text = my_font.render(turn_state, False, (0, 0, 0), (0,125,0) if turn_state == "DRAW" else (125,0,0))
        if game.players[player_turn].player_knock == True:
            turn_state = "KNOCK?"
            turn_text = my_font.render(turn_state, False, (0, 0, 0), (0,0,125))
        turn_text_position = (custom_border_width - turn_text.get_width() + custom_window_placement[0], custom_border_height + custom_window_placement[1] + (window_height - custom_border_height)/8) if player_turn == 0 else (custom_border_width - player_1_text.get_width() + custom_window_placement[0], custom_window_placement[1] - (window_height - custom_border_height)/3)
        window.blit(turn_text, turn_text_position)
        knock_button = None
        dont_knock_button = None
        if turn_state == "KNOCK?":
            knock_button = window.blit(my_font.render("YES", False, (0, 0, 0), (0,125,0)), (turn_text_position[0] - turn_text.get_width(), turn_text_position[1]))
            dont_knock_button = window.blit(my_font.render("NO", False, (0, 0, 0), (125,0,0)), (turn_text_position[0] - turn_text.get_width()/2, turn_text_position[1]))

        # Display player score
        player_1_score = my_font.render(f"Score: {game.players[0].score}", False, (0, 0, 0))
        window.blit(player_1_score, (custom_window_placement[0], custom_border_height + custom_window_placement[1] + (window_height - custom_border_height)/8))
        player_2_score = my_font.render(f"Score: {game.players[1].score}", False, (0, 0, 0))
        window.blit(player_2_score, (custom_window_placement[0], custom_window_placement[1] - (window_height - custom_border_height)/3))

        # Display game info
        round_num = game.round_number
        round_num_text = my_font.render(f"Round: {round_num}", False, (0, 0, 0))
        window.blit(round_num_text, (custom_window_placement[0], (custom_border_height - round_num_text.get_height()) / 2 + custom_window_placement[1]))
        cards_left = len(game.deck)
        cards_left_text = my_font.render(f"Deck size: {cards_left}", False, (0, 0, 0))
        window.blit(cards_left_text, (custom_window_placement[0], (custom_border_height + cards_left_text.get_height()) / 2 + custom_window_placement[1]))

        # Some logic where the player can interract with cards on the screen by clicking on them
        mouse_click_x, mouse_click_y = mouse_click_pos
        if deck_surface.collidepoint(mouse_click_x, mouse_click_y) and turn_state == "DRAW":
            out_q.put("random")
        elif discard_pile_surface.collidepoint(mouse_click_x, mouse_click_y) and turn_state == "DRAW":
            out_q.put("discard")

        player_card_i = 0
        for player_card_surface in player_card_surfaces[player_turn]:
            if player_card_surface.collidepoint(mouse_click_x, mouse_click_y) and turn_state == "DISCARD":
                out_q.put(player_card_i+1)
                break
            player_card_i += 1

        if turn_state == "KNOCK?" and not knock_button == None and not dont_knock_button == None:
            if knock_button.collidepoint(mouse_click_x, mouse_click_y):
                out_q.put("y")
            elif dont_knock_button.collidepoint(mouse_click_x, mouse_click_y):
                out_q.put("n")

    def display_loop(game, window):
        while True:
            mouse_click_pos = (0, 0)
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
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed()[0]: # Left click
                            mouse_click_pos = pygame.mouse.get_pos()
            except KeyboardInterrupt:
                break

            # Rendering
            window.fill((30, 92, 58))
            display_cards(game, window, mouse_click_pos)
            pygame.display.update()
            clock.tick(FPS)
    
    display_loop(game, window)
    pygame.quit()

def game_thread(game, in_q):
    game.game_flow(in_q)

def main():
    player1 = Player("Player 1")
    player2 = Player("Player 2")

    game = Gin_Rummy(player1, player2)

    q = Queue() # used for communicating between threads

    # Running game logic on a seperate daemon thread
    thread = threading.Thread(target=game_thread, args=(game, q, ), daemon=True)
    thread.start()

    # This main thread will be running the display
    pygame_display(game, q)
            

if __name__ == "__main__":
    main()
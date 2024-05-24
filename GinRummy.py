from BotManager import BotManager
from Deck import Deck
from HandEvaluator import HandEvaluator
from Player import Player
from Hand import Hand
from queue import Queue
from BarChart import BarChart
from DropDownMenu import DropDownMenu
from Button import Button
from Stats import Stats
import threading
import pygame
import sys
import time

class GinRummy(object):
    def __init__(self, player1, player2):
        #self.thread = threading
        self.players = [player1, player2]
        self.turn_index = 0 # 0 for player1, 1 for player2

        self.decline_round = True # the first round

        self.drawing_from_discard = False
        self.game_over = True
        self.game_exit = False
        self.strike_one = False
        self.short_of_card = False

        self.game_number = 0
        self.round_number = 0
        self.total_round_number = 0
        self.turn_number = 0

        self.deck = []
        self.discard_pile = []

        self.GIN_POINTS = 25
        self.UNDERCUT_POINTS = 10
        self.WINNING_SCORE = 100

        self.NORMAL_NUM_CARDS_PER_HAND = 10
        self.SMALLER_NUM_CARDS_PER_HAND = 7

        self.is_smaller_deck = False
        self.bot_manager = BotManager()
        self.hand_evaluator = HandEvaluator()

    def start_new_game(self, with_smaller_deck=True):
        self.game_number += 1
        self.is_smaller_deck = with_smaller_deck
        self.num_players_wanting_rematch = 0
        if self.game_over:
            self.round_number = 0
            for p in self.players:
                p.score = 0
                p.round_wins = 0
                p.wants_rematch = False
            self.game_over = False
            self.players[0].player_draw = True
            self.players[1].player_draw = False
            self.start_new_round()
    
    def start_new_round(self):
        self.round_number += 1
        self.total_round_number += 1
        self.turn_number = 0
        for p in self.players:
            p.hand = Hand()
            p.player_draw = False
            p.player_discard = False
            p.player_knock = False
            p.melds_in_hand_when_discard = []

            #A bit spaghetti, but it works
            if p.name == "CFR" or p.name == "GreedyBot" or p.name == "CFRBaseline" or p.name == "CFRKnocking" or p.name == "RandomBot" or p.name == "RandomBot2" or p.name == "GROCFR" or p.name == "DeepLearningCFR":
                p.is_human = False

        self.deck = Deck()
        if self.is_smaller_deck:
            self.deck.make_smaller_deck()
        self.deck.shuffle()
        self.deal(self.is_smaller_deck)
        self.discard_pile = []
        self.discard_pile.append(self.deck.deal())
        self.bot_manager = BotManager()

    def deal(self, with_smaller_deck=True):
        num_cards = self.NORMAL_NUM_CARDS_PER_HAND
        if with_smaller_deck:
            num_cards = self.SMALLER_NUM_CARDS_PER_HAND
        for i in range(num_cards):
            for p in self.players:
                p.hand.add(self.deck.deal())

    def draw(self, player, in_q):
        answering = False
        print("Your hand: ", player.hand.sort_by_rank())
        print("Top of discard pile: ", self.discard_pile[-1])
        print("Deck size: ", len(self.deck))
        time_diff = 0
        while answering == False:
            if player.name == "CFR" or player.name == "CFRKnocking":
                print(f"{player.name} is thinking...")
                start = time.time()
                answer = self.bot_manager.get_action_from_bot("draw", "SuperSimpleCFR", self, player.depth)
                end = time.time()
                time_diff = end - start
                print(f"{player.name} chose {answer} in {time_diff} seconds")
            elif player.name == "CFRBaseline":
                print(f"{player.name} is thinking...")
                start = time.time()
                answer = self.bot_manager.get_action_from_bot("draw", "SSCFRBaseline", self, player.depth)
                end = time.time()
                time_diff = end - start
                print(f"{player.name} chose {answer} in {time_diff} seconds")
            elif player.name == "GreedyBot":
                start = time.time()
                answer = self.bot_manager.get_action_from_bot("draw", "GreedyBot", self, player.depth)
                end = time.time()
                time_diff = end - start
                print(f"{player.name} chose {answer} in {time_diff} seconds")
            elif player.name == "GROCFR":
                start = time.time()
                answer = self.bot_manager.get_action_from_bot("draw", "GROCFR", self, player.depth)
                end = time.time()
                time_diff = end - start
                print(f"{player.name} chose {answer} in {time_diff} seconds")
            elif player.name == "DeepLearningCFR":
                start = time.time()
                answer = self.bot_manager.get_action_from_bot("draw", "DeepLearningCFR", self, player.depth)
                end = time.time()
                time_diff = end - start
                print(f"{player.name} chose {answer} in {time_diff} seconds")
            elif player.name == "RandomBot":
                answer = self.bot_manager.get_action_from_bot("draw", "RandomBot", self)
            elif player.name == "RandomBot2":
                answer = self.bot_manager.get_action_from_bot("draw", "BetterRandomBot", self)
            else:
                start = time.time()
                answer = in_q.get()
                end = time.time()
                time_diff = end - start
                print(f"{player.name} chose {answer} in {time_diff} seconds")

            answering = answer.lower() == "random" or answer.lower() == "discard"

        player.draw_times.append(time_diff)
        
        if answer.lower() == "random":
            card_drawn = self.deck.deal()
            player.hand.add(card_drawn)
            self.drawing_from_discard = False
            print(f"{player.name} drew: {player.hand.cards[-1]}")
        else:
            card_drawn = self.discard_pile.pop()
            card_drawn.just_drew = True
            player.hand.add(card_drawn)
            self.drawing_from_discard = True
            self.bot_manager.add_known_card(card_drawn, self.turn_index)

    def discard(self, player, in_q):
        print(f"{player.name} hand: {player.hand.sort_by_rank()}")
        check_if_int = False
        time_diff = 0
        while check_if_int == False:
            if player.name == "CFR" or player.name == "CFRKnocking":
                print(f"{player.name} is thinking...")
                start = time.time()
                answer = self.bot_manager.get_action_from_bot("discard", "SuperSimpleCFR", self, player.depth)
                end = time.time()
                time_diff = end - start
                print(f"{player.name} chose {answer} in {time_diff} seconds")
            elif player.name == "CFRBaseline":
                print(f"{player.name} is thinking...")
                start = time.time()
                answer = self.bot_manager.get_action_from_bot("discard", "SSCFRBaseline", self, player.depth)
                end = time.time()
                time_diff = end - start
                print(f"{player.name} chose {answer} in {time_diff} seconds")
            elif player.name == "GreedyBot":
                start = time.time()
                answer = self.bot_manager.get_action_from_bot("discard", "GreedyBot", self, player.depth)
                end = time.time()
                time_diff = end - start
                print(f"{player.name} chose {answer} in {time_diff} seconds")
            elif player.name == "GROCFR":
                start = time.time()
                answer = self.bot_manager.get_action_from_bot("discard", "GROCFR", self, player.depth)
                end = time.time()
                time_diff = end - start
                print(f"{player.name} chose {answer} in {time_diff} seconds")
            elif player.name == "DeepLearningCFR":
                start = time.time()
                answer = self.bot_manager.get_action_from_bot("discard", "DeepLearningCFR", self, player.depth)
                end = time.time()
                time_diff = end - start
                print(f"{player.name} chose {answer} in {time_diff} seconds")
            elif player.name == "RandomBot":
                answer = self.bot_manager.get_action_from_bot("discard", "RandomBot", self)
            elif player.name == "RandomBot2":
                answer = self.bot_manager.get_action_from_bot("discard", "BetterRandomBot", self)
            else:    
                answer = in_q.get()

            check_if_int = True
            try:
                int(answer)
            except ValueError:
                check_if_int = False

        best_meld = self.hand_evaluator.find_best_meld(player.hand)
        player.melds_in_hand_when_discard.append(0 if best_meld == None else len(best_meld))
        player.discard_times.append(time_diff)
        
        card = player.hand.cards[int(answer)-1]
        player.hand.cards.remove(card)
        self.discard_pile.append(card)
        self.drawing_from_discard = False
        self.bot_manager.remove_known_card(card, self.turn_index)

        for c in player.hand.cards:
            c.just_drew = False

        if self.hand_evaluator.get_hand_score(player.hand) <= 10:
            player.player_knock = True
            answering = False
            while answering == False:
                if player.name == "CFRKnocking":
                    knock_answer = self.bot_manager.get_knocking_action(self, "SuperSimpleCFR")
                elif player.name == "DeepLearningCFR":
                    knock_answer = self.bot_manager.get_knocking_action(self, "DeepLearningCFR")
                elif player.name == "CFRBaseline":
                    knock_answer = self.bot_manager.get_knocking_action(self, "SSCFRBaseline")
                elif player.name == "GROCFR":
                    knock_answer = self.bot_manager.get_knocking_action(self, "GROCFR")
                elif player.name == "GreedyBot" or player.name == "CFR" or player.name == "RandomBot" or player.name == "RandomBot2":
                    knock_answer = "y"
                else:  
                    knock_answer = in_q.get()
                answering = knock_answer.lower() == "y" or knock_answer.lower() == "n"

            if knock_answer.lower() == "y":
                self.knock(player, in_q)
            else:
                player.player_knock = False
                player.player_discard = False
                player.player_draw = True

        self.turn_index = (self.turn_index + 1) % 2
        if self.turn_index == 0:
            self.turn_number += 1
            print("Turn number: ", self.turn_number)

    def knock(self, player, in_q):
        player.total_knocks += 1

        for p in self.players:
            p.score_per_round.append(p.score)

        self.decline_round = False
        self.game_over = True
        self.strike_one = False
        self.short_of_card = False
        other_player = self.players[(self.turn_index + 1) % 2]

        print("------------------")
        print("Knocking player's hand score: ", player.hand.deadwood)
        print("Other player's hand score: ", other_player.hand.deadwood)
        print("------------------")

        deadwood = self.hand_evaluator.get_hand_score(player.hand)
        other_deadwood = self.hand_evaluator.get_hand_score(other_player.hand)
        if deadwood == 0:
            score = (other_deadwood - deadwood) + self.GIN_POINTS
            player.score += score
            player.total_score += score
            player.total_gins += 1
            player.round_wins += 1
        else:
            if deadwood < other_deadwood:
                score = other_player.hand.deadwood - player.hand.deadwood
                player.score += score
                player.total_score += score
                player.round_wins += 1
            else: # player.hand.deadwood > other_player.hand.deadwood
                score = deadwood - other_deadwood + self.UNDERCUT_POINTS
                other_player.score += score
                other_player.total_score += score
                other_player.total_undercuts += 1
                other_player.round_wins += 1

        print(f"{self.players[0].name}'s score: ", self.players[0].score)
        print(f"{self.players[1].name}'s score: ", self.players[1].score)

        bigger_score_player = player if player.score >= other_player.score else other_player

        if bigger_score_player.score >= self.WINNING_SCORE:
            self.game_over = True
            print(f"{bigger_score_player.name} won the game!")
            bigger_score_player.wins += 1

            for p in self.players:
                p.wins_per_game.append(p.wins)
                p.score_per_game.append(p.score)
                p.round_wins_per_game.append(p.round_wins)

            Stats.plot(self.game_number, [self.players[0], self.players[1]])
            Stats.finalize_plot(self.players[0].name, self.players[1].name)

            # Give option to restart, go to main menu, see stats or close the game
            what_to_do = ["", ""]
            possible_answers = ["rematch", "quit"]
            while what_to_do[0].split("_")[-1] not in possible_answers or what_to_do[1].split("_")[-1] not in possible_answers:
                for i in range(len(self.players)):
                    # If player i is a bot
                    if self.players[i].is_human == False:
                        if self.players[i].max_games > self.game_number:
                            what_to_do[i] = f"p{i}_rematch"
                            self.players[i].wants_rematch = True
                        else:
                            what_to_do[i] = f"p{i}_quit"
                            self.players[i].wants_rematch = False
                    else:
                        temp_val = in_q.get()
                        if temp_val.split("_")[0] != f"p{i}":
                            in_q.put(temp_val)
                        else:
                            what_to_do[i] = temp_val
            
            print(f"P1 wants {what_to_do[0]}")
            print(f"P2 wants {what_to_do[1]}")

            if what_to_do[0].split("_")[-1] == "rematch" and what_to_do[1].split("_")[-1] == "rematch":
                self.start_new_game()
            else:
                self.game_exit = True

        else:
            self.game_over = False
            self.strike_one = False
            self.short_of_card = False
            self.start_new_round()

    def game_flow(self, in_q):
        self.start_new_game(True)
        print("------------------")
        print("Game started")
        print("------------------")

        while self.game_exit == False:
            print("Round number: ", self.round_number)
            print(self.players[self.turn_index].name, "'s turn")
            self.draw(self.players[self.turn_index], in_q)
            self.discard(self.players[self.turn_index], in_q)

            # Check if the deck has only 2 cards left, in which case, the game ends in a draw
            if len(self.deck) <= 2:
                self.game_over = False
                self.start_new_round()

            print("Next turn")

def main_menu_display(window, clock, FPS, player1_name=["Player 1"], player2_name=["Player 2"], player1_depth=["8"], player2_depth=["8"]):
    def display_loop(window, player1_name, player2_name, player1_depth, player2_depth):
        # Title
        my_font = pygame.font.SysFont('Comic Sans MS', 50)
        title = my_font.render("Gin Rummy", False, (255, 255, 255))

        # Start button
        start_button = Button("Start", 200, 50)

        # Dropdown menu
        main_menu_dropdown_p1 = DropDownMenu("main_menu_dropdown_p1", ["Player 1", "GreedyBot", "CFR", "GROCFR", "DeepLearningCFR", "RandomBot2"], 200, 50) #RandomBot, RandomBot2 CFRKnocking, CFRBaseline
        main_menu_dropdown_p2 = DropDownMenu("main_menu_dropdown_p2", ["Player 2", "GreedyBot", "CFR", "GROCFR", "DeepLearningCFR", "RandomBot2"], 200, 50)

        # Depth dropdown menu
        main_menu_depth_p1 = DropDownMenu("main_menu_depth_p1", ["6", "8", "10"], 50, 50)
        main_menu_depth_p2 = DropDownMenu("main_menu_depth_p2", ["6", "8", "10"], 50, 50)

        # Main menu loop
        start_game = False
        while start_game == False:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                    if event.type == pygame.VIDEORESIZE:
                        window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1: # Left click
                            main_menu_dropdown_p1.process_click(event.pos)
                            main_menu_dropdown_p2.process_click(event.pos)
                            main_menu_depth_p1.process_click(event.pos)
                            main_menu_depth_p2.process_click(event.pos)
                            if start_button.collidepoint(event.pos):
                                player1_name[0] = main_menu_dropdown_p1.selected_item
                                player2_name[0] = main_menu_dropdown_p2.selected_item
                                player1_depth[0] = main_menu_depth_p1.selected_item
                                player2_depth[0] = main_menu_depth_p2.selected_item
                                start_game = True
            except KeyboardInterrupt:
                pygame.quit()
                sys.exit()

            window.fill((30, 92, 58))
            window.blit(title, (window.get_width()//2 - title.get_width()//2, window.get_height()//2 - 200))
            start_button.draw(window, window.get_width()//2 - 100, window.get_height()//2 - 25)
            main_menu_dropdown_p1.draw(window, window.get_width()//2 - 210, window.get_height()//2 + 50)
            main_menu_dropdown_p2.draw(window, window.get_width()//2 + 10, window.get_height()//2 + 50)
            main_menu_depth_p1.draw(window, window.get_width()//2 - 50 - 240, window.get_height()//2 + 50)
            main_menu_depth_p2.draw(window, window.get_width()//2 + 230, window.get_height()//2 + 50)
            pygame.display.update()
            clock.tick(FPS)
    
    display_loop(window, player1_name, player2_name, player1_depth, player2_depth)

def pygame_display(game, out_q, window, clock, FPS):        
    def display_cards(game, window, mouse_click_pos):
        # Define some useful variables
        window_width, window_height = window.get_size()
        screen_width, screen_height = pygame.display.get_desktop_sizes()[0]
        custom_border_width, custom_border_height = (window_width * 0.5, window_height * 0.7)
        custom_window_placement = (window_width/2 - custom_border_width/2, window_height/2 - custom_border_height/2)
        padding = 2

        mouse_click_x, mouse_click_y = mouse_click_pos
        if game.game_over == False:
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
                discard_pile_card = pygame.image.load('images/' + game.discard_pile[-1].suit + '_' + str(game.discard_pile[-1].value) + '.svg')
                discard_pile_card = pygame.transform.scale(discard_pile_card, (int(resized_card_width), int(resized_card_height)))
            discard_pile_surface = window.blit(discard_pile_card, (custom_border_width / 2 - resized_card_width - padding + custom_window_placement[0], (custom_border_height - resized_card_height) / 2 + custom_window_placement[1]))

            # Display cards in hand
            player_card_surfaces = []
            player_i = 1
            for player in game.players:
                card_i = 0
                current_player_card_surfaces = []
                for card in player.hand.cards:
                    image = pygame.image.load('images/' + card.suit + '_' + str(card.value) + '.svg')
                    # If card isHidden, we want to not show it
                    if card.isHidden:
                        image = card_back
                    # Transform card's size
                    image = pygame.transform.scale(image, (int(resized_card_width), int(resized_card_height)))
                    # Render card on screen
                    card_surface = window.blit(image,
                    ((resized_card_width + padding) * card_i + (custom_border_width/2 - resized_card_width*(len(player.hand.cards) / 2) + custom_window_placement[0]),
                    (custom_border_height - resized_card_height) * player_i + custom_window_placement[1]))
                    card_i += 1
                    current_player_card_surfaces.append(card_surface)
                player_card_surfaces.append(current_player_card_surfaces)
                player_i -= 1

            # Display player text
            my_font = pygame.font.SysFont('Comic Sans MS', 20)
            player_1_text = my_font.render(game.players[0].name, False, (0, 0, 0))
            window.blit(player_1_text, (custom_border_width/2 - player_1_text.get_width()/2 + custom_window_placement[0], custom_border_height + custom_window_placement[1] + (window_height - custom_border_height)/8))
            player_2_text = my_font.render(game.players[1].name, False, (0, 0, 0))
            window.blit(player_2_text, (custom_border_width/2 - player_1_text.get_width()/2 + custom_window_placement[0], custom_window_placement[1] - (window_height - custom_border_height)/3))

            my_font = pygame.font.SysFont('Comic Sans MS', 10)
            player_1_text = my_font.render(f"{game.players[0].total_score}", False, (0, 0, 0))
            window.blit(player_1_text, (custom_border_width/2 - player_1_text.get_width()/2 + custom_window_placement[0], custom_border_height + custom_window_placement[1] + (window_height - custom_border_height)/8))
            player_2_text = my_font.render(f"{game.players[1].total_score}", False, (0, 0, 0))
            window.blit(player_2_text, (custom_border_width/2 - player_1_text.get_width()/2 + custom_window_placement[0], custom_window_placement[1] - (window_height - custom_border_height)/3))


            # Display player turn
            my_font = pygame.font.SysFont('Comic Sans MS', 20)
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
            
            # Some logic where the player can interract with cards on the screen by clicking on them
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
        else:
            # Display restart options and stuff
            num_players_wanting_rematch = 0
            for p in game.players:
                if p.wants_rematch == True:
                    num_players_wanting_rematch += 1
            my_font = pygame.font.SysFont('Comic Sans MS', 20)
            restart_text = my_font.render(f"Do you want a rematch? {num_players_wanting_rematch}/2", False, (0, 0, 0))
            window.blit(restart_text, (custom_window_placement[0] + custom_border_width/2 - restart_text.get_width()/2, (custom_border_height - restart_text.get_height()) / 2 + custom_window_placement[1]))

            p_rematch_button = [None, None]
            p_quit_button = [None, None]
            for i, p in enumerate(game.players):
                if p.is_human == True:
                    restart_text = my_font.render("REMATCH", False, (0, 0, 0), (0,125,0))
                    quit_text = my_font.render("QUIT", False, (0, 0, 0), (125,0,0))
                    p_rematch_button[i] = window.blit(restart_text, (custom_window_placement[0] + custom_border_width/2 - (restart_text.get_width() + quit_text.get_width())/2, (custom_border_height - restart_text.get_height()) / 2 + custom_window_placement[1] + custom_border_height/4 * (-1 if i == 1 else 1)))
                    p_quit_button[i] = window.blit(quit_text, (custom_window_placement[0] + custom_border_width/2 - (restart_text.get_width() + quit_text.get_width())/2 + restart_text.get_width() + padding, (custom_border_height - restart_text.get_height()) / 2 + custom_window_placement[1] + custom_border_height/4 * (-1 if i == 1 else 1)))

                if p_rematch_button[i] != None and p_quit_button[i] != None:
                    if p_rematch_button[i].collidepoint(mouse_click_x, mouse_click_y):
                        out_q.put(f"p{i}_rematch")
                        p.wants_rematch = True
                    elif p_quit_button[i].collidepoint(mouse_click_x, mouse_click_y):
                        out_q.put(f"p{i}_quit")
                        p.wants_rematch = False
        
        player_1_wins = my_font.render(f"Wins: {game.players[0].wins}", False, (0, 0, 0))
        window.blit(player_1_wins, (custom_window_placement[0], custom_border_height + custom_window_placement[1] + (window_height - custom_border_height)/8 - player_1_wins.get_height()))
        player_2_wins = my_font.render(f"Wins: {game.players[1].wins}", False, (0, 0, 0))
        window.blit(player_2_wins, (custom_window_placement[0], custom_window_placement[1] - (window_height - custom_border_height)/3 + player_2_wins.get_height()))

        game_num = game.game_number
        game_num_text = my_font.render(f"Game: {game_num}", False, (0, 0, 0))
        window.blit(game_num_text, (custom_window_placement[0], (custom_border_height - game_num_text.get_height()*2) / 2 + custom_window_placement[1]))
        round_num = game.round_number
        round_num_text = my_font.render(f"Round: {round_num}", False, (0, 0, 0))
        window.blit(round_num_text, (custom_window_placement[0], (custom_border_height) / 2 + custom_window_placement[1]))
        total_round_num = game.total_round_number
        total_round_num_text = my_font.render(f"Total rounds: {total_round_num}", False, (0, 0, 0))
        window.blit(total_round_num_text, (custom_window_placement[0], (custom_border_height + total_round_num_text.get_height()*2) / 2 + custom_window_placement[1]))

    def display_loop(game, window):
        # For drag and drop
        move_box = None
        inflate_box = None

        # This is just a test chart, will be updated soon
        # test_chart = BarChart("testChart", 200, 200,  window.get_width() // 2, 0, [1,2,3,4,10,18,24], [4,3,9,2,7,12,5], 1)
        
        while True:
            mouse_click_pos = (0, 0)
            # Handle interrupts, window resizes and "quit" events
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                    if event.type == pygame.VIDEORESIZE:
                        window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1: # Left click
                            mouse_click_pos = pygame.mouse.get_pos()
                            # if test_chart.collidepoint(event.pos):
                            #     move_box = test_chart
                        if event.button == 3: # Right click
                            # if test_chart.collidepoint(event.pos):
                            #     inflate_box = test_chart
                            pass
                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1: # Left click
                            move_box = None
                        if event.button == 3: # Right click
                            inflate_box = None
                    if event.type == pygame.MOUSEMOTION:
                        if move_box != None:
                            move_box.move_ip(event.rel, window.get_width()//2, window.get_width(), 0, window.get_height())
                        if inflate_box != None:
                            inflate_box.inflate(event.rel, 400, 400)

            except KeyboardInterrupt:
                pygame.quit()
                sys.exit()

            # Rendering
            window.fill((30, 92, 58))
            display_cards(game, window, mouse_click_pos)
            # test_chart.draw(window)
            pygame.display.update()
            clock.tick(FPS)
    
    display_loop(game, window)

def game_thread(game, in_q):
    game.game_flow(in_q)

def main():
    pygame.init()
    bounds = (1500, 500)
    window = pygame.display.set_mode(bounds, pygame.RESIZABLE)
    pygame.display.set_caption("Gin Rummy")
    clock = pygame.time.Clock()
    FPS = 12

    # Init font
    pygame.font.init()

    p1_name = ["Player 1"]
    p2_name = ["Player 2"]

    p1_depth = ["8"]
    p2_depth = ["8"]

    # Before we start the game, we have to promt the main menu screen where player can choose bots etc.
    main_menu_display(window, clock, FPS, p1_name, p2_name, p1_depth, p2_depth)

    player1 = Player(p1_name[0], int(p1_depth[0]))
    player2 = Player(p2_name[0], int(p2_depth[0]))

    game = GinRummy(player1, player2)

    q = Queue() # used for communicating between threads

    # Running game logic on a seperate daemon thread
    # game.thread = threading.Thread(target=game_thread, args=(game, q, ), daemon=False)
    # game.thread.start()

    # This main thread will be running the display
    #pygame_display(game, q, window, clock, FPS)
    pygame.quit()
    game_thread(game, q)

if __name__ == "__main__":
    main()
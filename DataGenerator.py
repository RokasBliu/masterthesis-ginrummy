from GinRummy import GinRummy
from Player import Player
import random
import pandas as pd
from Card import Card
from GameState import GameState
class DataGenerator:
    def __init__(self):
        #Using CFR with depth 8 to create data
        self.bot = "SuperSimpleCFR"
        self.data_amount = 5000
        pass

    def create_random_game_state(self, stage = "draw"):
        main_player = Player("main player")
        oponent_player = Player("opponent player")
        rand_game = GinRummy(main_player, oponent_player)
        rand_game.start_new_game()

        turn_number = random.randint(0, 20)
        
        if stage == "draw":
            for i in range(turn_number):
                print("Round number: ", rand_game.round_number)
                print(rand_game.players[rand_game.turn_index].name, "'s turn")
                self.draw_rand_state(rand_game, rand_game.players[rand_game.turn_index])
                self.discard_rand_state(rand_game, rand_game.players[rand_game.turn_index])

        else:
            for i in range(turn_number):
                print("Round number: ", rand_game.round_number)
                print(rand_game.players[rand_game.turn_index].name, "'s turn")
                self.draw_rand_state(rand_game, rand_game.players[rand_game.turn_index])
                self.discard_rand_state(rand_game, rand_game.players[rand_game.turn_index])
            
            self.draw_rand_state(rand_game, main_player)
                

        rand_game_state = GameState(rand_game, "draw", rand_game.bot_manager.known_cards_p1)
        phantom_card_number = random.randint(0, 2)
        for i in range(phantom_card_number):
            phantom_card = Card("", "")
            phantom_card.make_phantom_card(rand_game_state.rand_card_dist)
            main_player.hand.add(phantom_card)
            self.discard_rand_state(rand_game, main_player) 
        return rand_game

    
    def draw_rand_state(self, game, player):
        player.total_turns += 1
        print("Your hand: ", player.hand.sort_by_rank())
        print("Top of discard pile: ", game.discard_pile[-1])
        print("Deck size: ", len(game.deck))

        answers = ["random", "discard"]
        rand_num = random.randint(0,1)
        answer = answers[rand_num]

        if answer == "random":
            card_drawn = game.deck.deal()
            player.hand.add(card_drawn)
            game.drawing_from_discard = False
        
        else:
            card_drawn = game.discard_pile.pop()
            card_drawn.just_drew = True
            player.hand.add(card_drawn)
            game.drawing_from_discard = True
            game.bot_manager.add_known_card(card_drawn, game.turn_index)

    def discard_rand_state(self, game, player):
        rand_num = random.randint(0,6)
        card = player.hand.cards[rand_num]
        player.hand.cards.remove(card)
        game.discard_pile.append(card)
        game.drawing_from_discard = False
        game.bot_manager.remove_known_card(card, game.turn_index)

        if card in game.bot_manager.known_cards_p1:
            game.bot_manager.known_cards_p1.remove(card)

        for c in player.hand.cards:
            c.just_drew = False
        
        game.turn_index = (game.turn_index + 1) % 2
        if game.turn_index == 0:
            game.turn_number += 1
            print("Turn number: ", game.turn_number)

    def create_data_from_game_state(self, state, stage, player, known_cards):
        data_array = []
        data_array.append(player.hand.cards)
        data_array.append(known_cards)
        data_array.append(state.discard_pile)
        data_array.append(state.turn_number)
        predicted_score = state.bot_manager.get_action_from_bot(stage, self.bot, state, return_number_value = True)
        data_array.append(predicted_score)

        return data_array

    def print_state(self, state):
        print("Player hand: ", state.players[0].hand)
        print("Discard pile: ", state.discard_pile)
        print("Turn number: ", state.turn_number)
        print("Known cards: ", state.bot_manager.known_cards_p1)
    
def main():
    data_gen = DataGenerator()
    data = []
    for i in range(data_gen.data_amount):
        game = data_gen.create_random_game_state("draw")
        data_gen.print_state(game)
        data.append(data_gen.create_data_from_game_state(game, "draw", game.players[0], game.bot_manager.known_cards_p1))
    for i in range(data_gen.data_amount):
        game = data_gen.create_random_game_state("discard")
        data_gen.print_state(game)
        data.append(data_gen.create_data_from_game_state(game, "discard", game.players[0], game.bot_manager.known_cards_p1))

    for d in data:
        print(d)
    df = pd.DataFrame(data, columns=["Player Hand", "Known Cards", "Discard Pile", "Turn Number", "Predicted Score"])
    print(df)
    df.to_csv("test-data-draw-2.csv")
    #df.to_excel("test-data.xlsx")

main()

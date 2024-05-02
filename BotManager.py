from GROCFR import GROCFR
from GameState import GameState
from SSCFRBaseline import SSCFRBaseline
from SuperSimpleCFR import SuperSimpleCFR
from GreedyBot import GreedyBot
class BotManager:
    def __init__(self):
        self.known_cards_p1 = []
        self.known_cards_p2 = []
        self.bots = ["SSCFRBaseline", "SuperSimpleCFR", "GreedyBot", "GROCFR"]
    
    def check_if_bot_exists(self, bot):
        for b in self.bots:
            if b == bot:
                return True
        return False

    def add_known_card(self, card, turn_index):
        if turn_index == 0:
            self.known_cards_p2.append(card)
        else:
            self.known_cards_p1.append(card)
        
        print("Known cards p1: ", self.known_cards_p1)
        print("Known cards p2: ", self.known_cards_p2)

    def remove_known_card(self, card, turn_index):
        if turn_index == 0:
            if card in self.known_cards_p2:
                self.known_cards_p2.remove(card)
        else:
            if card in self.known_cards_p1:
                self.known_cards_p1.remove(card)
    
    def get_action_from_bot(self, stage, bot, game, layers=8):
        if game.turn_index == 0:
            known_cards = self.known_cards_p1
        else:
            known_cards = self.known_cards_p2
        
        game_state = GameState(game, stage, known_cards)

        if bot == "SuperSimpleCFR":
            sscfr = SuperSimpleCFR()
            return sscfr.resolve(game_state, "end_game", layers, 1)
        elif bot == "SSCFRBaseline":
            sscfr = SSCFRBaseline()
            return sscfr.resolve(game_state, "end_game", 8, 1)
        elif bot == "GreedyBot":
            gb = GreedyBot()
            return gb.get_action(game_state)
        elif bot == "GROCFR":
            grocfr = GROCFR()
            return grocfr.resolve(game_state, "end_game", layers, 1)
        else:
            print("Bot not found")
        
    def get_knocking_action(self, game, bot):
        if bot == "SuperSimpleCFR":
            game_state = GameState(game, "draw", [])
            sscfr = SuperSimpleCFR()
            return sscfr.knocking_strategy_rule_based(game_state)
        if bot == "GROCFR":
            game_state = GameState(game, "draw", [])
            grocfr = GROCFR()
            return grocfr.knocking_strategy_rule_based(game_state)
        else:
            return "y"
from GameState import GameState
from SuperSimpleCFR import SuperSimpleCFR
from GreedyBot import GreedyBot
class BotManager:
    def __init__(self):
        self.known_cards = []
        self.bots = ["SuperSimpleCFR", "GreedyBot"]
        pass
    
    def check_if_bot_exists(self, bot):
        for b in self.bots:
            if b == bot:
                return True
        return False

    def add_known_card(self, card, player):
        if player.is_human:
            self.known_cards.append(card)

    def remove_known_card(self, card):
        if card in self.known_cards:
            self.known_cards.remove(card)

    def get_action_from_bot(self, stage, bot, game):
        game_state = GameState(game, stage, self.known_cards)

        if bot == "SuperSimpleCFR":
            sscfr = SuperSimpleCFR()
            return sscfr.resolve(game_state, "end_game", 8, 1)

        elif bot == "GreedyBot":
            gb = GreedyBot()
            return gb.get_action(game_state)
        else:
            print("Bot not found")
            return 
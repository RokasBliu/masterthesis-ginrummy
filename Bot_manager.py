from Game_State import Game_State
from Super_Simple_CFR import Super_Simple_CFR
from Greedy_Bot import Greedy_Bot
class Bot_Manager:
    def __init__(self):
        self.known_cards = []
        self.bots = ["Super_Simple_CFR", "Greedy_Bot"]
        pass
    
    def check_if_bot_exists(self, bot):
        for b in self.bots:
            if b == bot:
                return True
        return False

    def add_known_card(self, card, player):
        if player.is_human:
            self.known_cards.append(card)

    def get_action_from_bot(self, stage, bot, game):
        game_state = Game_State(game, stage, self.known_cards)

        if bot == "Super_Simple_CFR":
            sscfr = Super_Simple_CFR()
            return sscfr.resolve(game_state, "end_game", 8, 1)

        elif bot == "Greedy_Bot":
            gb = Greedy_Bot()
            return gb.get_action(game_state)
        else:
            print("Bot not found")
            return 
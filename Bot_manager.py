from Game_State import Game_State
from Super_Simple_CFR import Super_Simple_CFR
class Bot_Manager:
    def __init__(self):
        self.known_cards = []
        pass

    def get_action_from_bot(self, stage, bot, game):
        game_state = Game_State(game, stage)

        if bot == "Super_Simple_CFR":
            sscfr = Super_Simple_CFR()
            return sscfr.resolve(game_state, "end_game", 8, 1)
    
        else:
            print("Bot not found")
            return 
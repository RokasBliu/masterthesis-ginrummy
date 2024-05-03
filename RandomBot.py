from random import randint

class RandomBot():
    def __init__(self):
        self.action_draw = ["draw", "discard"]
        
    def get_action(self, game_state):
        assert game_state.main_player_index == game_state.turn_index

        hand = game_state.main_player_hand

        if game_state.state == "draw":
            rand_action = self.action_draw[randint(0, 1)]

            return rand_action
        
        elif game_state.state == "discard":
            return randint(1, len(hand.cards))
            
        else:
            # Instantly knock otherwise
            return "y"
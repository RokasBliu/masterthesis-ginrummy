import copy
class Greedy_Bot:
    def __init__(self, game):
        self.actions = []

    def get_action(self, game_state):
        assert game_state.main_player_index == game_state.turn_index

        hand = game_state.main_player_hand
        hand_deadwood = hand.get_hand_score()
        best_deadwood = 100

        if game_state.state == "draw":
            temp_hand = copy.deepcopy(hand)
            temp_hand.add(game_state.top_card_discard_pile)
            discard_deadwood = temp_hand.get_hand_score()
            if discard_deadwood < hand_deadwood:
                return "draw_discard"
            else:
                return "draw_deck"
        
        elif game_state.state == "discard":

            best_card = None
            best_index = 0
            for i in range (len(hand)):
                temp_hand = copy.deepcopy(hand)
                temp_hand.remove(hand[i])
                deadwood = temp_hand.get_hand_score()
                if deadwood < best_deadwood:
                    best_deadwood = deadwood
                    best_card = hand[i]
                    best_index = i
        else:
            return "knock"
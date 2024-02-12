import copy
class Greedy_Bot:
    def __init__(self):
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
                return "discard"
            else:
                return "random"
        
        elif game_state.state == "discard":
            best_index = 0
            for i in range(len(hand.cards) - 1, -1, -1):
                temp_hand = copy.deepcopy(hand)
                temp_hand.cards.remove(temp_hand.cards[i])
                deadwood = temp_hand.get_hand_score()
                if deadwood < best_deadwood:
                    best_deadwood = deadwood
                    best_index = i
            print("Worst card: ", hand.cards[best_index])
            return best_index + 1
        else:
            # Instantly knock otherwise
            return "y"
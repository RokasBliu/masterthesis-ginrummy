import copy
from HandEvaluator import HandEvaluator

class GreedyBot:
    def __init__(self):
        self.hand_evaluator = HandEvaluator()

    def get_action(self, game_state):
        assert game_state.main_player_index == game_state.turn_index

        hand = game_state.main_player_hand
        hand_deadwood = self.hand_evaluator.get_hand_score(game_state.main_player_hand)
        best_deadwood = 100

        if game_state.state == "draw":
            temp_hand = copy.deepcopy(hand)
            temp_hand.add(game_state.top_card_discard_pile)
            discard_deadwood = self.hand_evaluator.get_hand_score(temp_hand)
            if discard_deadwood < hand_deadwood:
                return "discard"
            else:
                return "random"
        
        elif game_state.state == "discard":

            best_index = 0
            for i in range(len(hand.cards)):
                temp_hand = copy.deepcopy(hand)
                temp_hand.cards.remove(hand.cards[i])
                deadwood = self.hand_evaluator.get_hand_score(temp_hand)
                if deadwood < best_deadwood:
                    best_deadwood = deadwood
                    best_index = i
            
            return best_index + 1
        else:
            # Instantly knock otherwise
            return "y"
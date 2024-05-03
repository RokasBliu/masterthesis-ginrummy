from random import randint

class BetterRandomBot():
    def __init__(self):
        self.action_draw = ["draw", "discard"]
        
    def get_action(self, game_state):
        assert game_state.main_player_index == game_state.turn_index

        hand = game_state.main_player_hand

        if game_state.state == "draw":
            return "random"
        
        elif game_state.state == "discard":
            hand_evaluator = game_state.oracle.hand_evaluator
            deadwood, best_meld = hand_evaluator.get_hand_score(game_state.main_player_hand, True)

            x = 0
            while x < 1000:
                discard_index = randint(0, len(hand.cards) - 1)
                if best_meld == []:
                    x += 1
                    continue
                if hand.cards[discard_index] not in best_meld[-1]:
                        print("Best Meld: ", best_meld)
                        return discard_index + 1

                x += 1
            
            print("-----------------")
            print("Best Meld: ", best_meld)
            print("-----------------")

            return discard_index + 1
                              
        else:
            # Instantly knock otherwise
            return "y"
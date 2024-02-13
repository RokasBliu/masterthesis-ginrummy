from BotManager import BotManager
from GinRummy import GinRummy


class BattleSimulator:
    def __init__(self):
        pass

    def simulate_battle(self, bot1, bot2, iterations=10):
        # Create a new game
        bot_manager = BotManager()
        bot1_wins = 0
        bot2_wins = 0
        for b in [bot1, bot2]:
            if not bot_manager.check_if_bot_exists(b):
                print(f"Bot {b} does not exist")
                return

            
        for i in range(iterations):
            game = GinRummy(bot1, bot2)
            game.game_flow(None)
            print(f"Game {i} finished")
from Hand import Hand

class Player(object):
    def __init__(self, name, depth=8):
        self.name = name
        self.hand = Hand()
        self.score = 0
        self.wins = 0
        self.round_wins = 0
        self.is_human = True
        self.max_games = 100
        self.player_knock = False
        self.player_draw = True # True when it is player's turn to draw; False when it is not
        self.player_discard = False # True when it is player's turn to discard; False when it is not
        self.in_play = False
        self.wants_rematch = False
        self.depth = depth

        self.draw_times = []
        self.discard_times = []
        self.melds_in_hand_when_discard = []

        self.wins_per_game = []
        self.score_per_game = []
        self.score_per_round = []
        self.round_wins_per_game = []
        self.total_undercuts = 0
        self.total_gins = 0
        self.total_knocks = 0
        self.total_score = 0
    
    def get_total_round_wins(self):
        return '{0:.3g}'.format(sum(self.round_wins_per_game))

    def get_avg_score_per_game(self):
        return '{0:.3g}'.format(sum(self.score_per_game) / len(self.score_per_game))
    
    def get_avg_score_per_round(self):
        return '{0:.3g}'.format(sum(self.score_per_round) / len(self.score_per_round))
    
    def get_winrate(self):
        return '{0:.3g}%'.format(self.wins * 100 / len(self.wins_per_game)) 
    
    def get_round_winrate_per_game(self):
        return '{0:.3g}'.format(sum(self.round_wins_per_game) / len(self.round_wins_per_game))
    
    def get_avg_draw_time(self):
        return '{0:.3g}'.format(sum(self.draw_times) / len(self.draw_times))
    
    def get_avg_discard_time(self):
        return '{0:.3g}'.format(sum(self.discard_times) / len(self.discard_times))

    def get_avg_turn_times_per_meld_cards_in_hand(self):
        times = []
        i = 0
        while i < max(self.melds_in_hand_when_discard, default=-1) + 1:
            times.extend([[]])
            i += 1
        for idx, element in enumerate(self.melds_in_hand_when_discard):
            times[element].append(self.draw_times[idx] + self.discard_times[idx])
        avg_times = []
        for times_per_meld_count in times:
            avg_times.append(0 if len(times_per_meld_count) == 0 else sum(times_per_meld_count) / len(times_per_meld_count))
        return avg_times

    def __repr__(self):
        return f"{self.name} has a score of {self.score}, with a hand of {self.hand}"
    
    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name
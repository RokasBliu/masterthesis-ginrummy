from Hand import Hand

class Player(object):
    def __init__(self, name):
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

        self.total_turns = 0
        self.avg_draw_time = 0
        self.avg_discard_time = 0

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
        return '{0:.3g}'.format(self.avg_draw_time)
    
    def get_avg_discard_time(self):
        return '{0:.3g}'.format(self.avg_discard_time)

    def __repr__(self):
        return f"{self.name} has a score of {self.score}, with a hand of {self.hand}"
    
    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name
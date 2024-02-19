from Hand import Hand

class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = Hand()
        self.score = 0
        self.wins = 0
        self.is_human = True
        self.max_games = 100
        self.player_knock = False
        self.player_draw = True # True when it is player's turn to draw; False when it is not
        self.player_discard = False # True when it is player's turn to discard; False when it is not
        self.in_play = False
        self.wants_rematch = False

    def __repr__(self):
        return f"{self.name} has a score of {self.score}, with a hand of {self.hand}"
    
    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name
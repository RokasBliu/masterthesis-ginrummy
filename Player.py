class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.score = 0
        self.isHuman = True

    def __repr__(self):
        return f"{self.name} has a score of {self.score}"
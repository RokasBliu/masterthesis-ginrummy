class Action:
    def __init__(self, name, description, player):
        self.name = name
        self.player = player
        self.description = description

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name}: {self.description} by {self.player}"

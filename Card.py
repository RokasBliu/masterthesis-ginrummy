import pygame

class Card(object):
        def __init__(self, suit, value):
            self.suit = suit
            self.value = value
            self.image = pygame.image.load('images/' + self.suit + '_' + str(self.value) + '.svg')
            self.hidden = True
            self.meld_ids = []

        def __repr__(self):
            return f"{self.value} of {self.suit} ({self.meld_ids})"
        
        def __eq__(self, other):
            return self.value == other.value and self.suit == other.suit
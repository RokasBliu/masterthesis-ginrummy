import random
import pygame

class Card(object):
        def __init__(self, suit, value):
            self.suit = suit
            self.value = value
            self.image = pygame.image.load('images/' + str(self.value) + '_of_' + self.suit + '.svg')
            self.hidden = True
            self.meld_ids = []

        def __repr__(self):
            return f"{self.value} of {self.suit} ({self.meld_ids})"
        
        def __eq__(self, other):
            return self.value == other.value and self.suit == other.suit

class Deck(list):

        def __init__(self):
            self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
            self.values = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
            for suit in self.suits:
                for value in self.values:
                    self.append(Card(suit, value))
        
        def shuffle(self):
            random.shuffle(self)
        
        def deal(self):
            return self.pop(0)

        def make_smaller_deck(self): # For easier computations
            self.clear()
            self.values = ['5','6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
            for suit in self.suits:
                for value in self.values:
                    self.append(Card(suit, value))
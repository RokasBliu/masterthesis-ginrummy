class Card(object):
        def __init__(self, suit, value):
            self.suit = suit
            self.value = value
            self.isHidden = False
            self.isPhantom = False
            self.phantom_values = []
            self.meld_ids = []

        def make_phantom_card(self, phantom_values):
            self.suit = None
            self.value = None
            self.isPhantom = True
            self.phantom_values = phantom_values

        def __repr__(self):
            if self.isPhantom:
                return f"Phantom Card: {self.phantom_values}"
            return f"{self.value} of {self.suit}" #meld ids: {self.meld_ids}
        
        def __eq__(self, other):
            return self.value == other.value and self.suit == other.suit
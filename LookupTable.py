class LookupTable:
    def __init__(self):

        self.three_of_a_kind = {
            ("3", "3", "3"): 9,
            ("4", "4", "4"): 12,
            ("5", "5", "5"): 15,
            ("6", "6", "6"): 18,
            ("7", "7", "7"): 21,
            ("8", "8", "8"): 24,
            ("9", "9", "9"): 27,
            ("10", "10", "10"): 30,
            ("Jack", "Jack", "Jack"): 30,
            ("Queen", "Queen", "Queen"): 30,
            ("King", "King", "King"): 30,
            ("Ace", "Ace", "Ace"): 30
        }

        self.four_of_a_kind = {
            ("3", "3", "3", "3"): 12,
            ("4", "4", "4", "4"): 16,
            ("5", "5", "5", "5"): 20,
            ("6", "6", "6", "6"): 24,
            ("7", "7", "7", "7"): 28,
            ("8", "8", "8", "8"): 32,
            ("9", "9", "9", "9"): 36,
            ("10", "10", "10", "10"): 40,
            ("Jack", "Jack", "Jack", "Jack"): 40,
            ("Queen", "Queen", "Queen", "Queen"): 40,
            ("King", "King", "King", "King"): 40,
            ("Ace", "Ace", "Ace", "Ace"): 40
        }

        self.straight_three = {
            ("3", "4", "5"): 6,
            ("4", "5", "6"): 9,
            ("5", "6", "7"): 12,
            ("6", "7", "8"): 15,
            ("7", "8", "9"): 18,
            ("8", "9", "10"): 21,
            ("9", "10", "Jack"): 24,
            ("10", "Jack", "Queen"): 27,
            ("Jack", "Queen", "King"): 30,
            ("Queen", "King", "Ace"): 33
        }

        self.straight_four = {
            ("3", "4", "5", "6"): 8,
            ("4", "5", "6", "7"): 12,
            ("5", "6", "7", "8"): 16,
            ("6", "7", "8", "9"): 20,
            ("7", "8", "9", "10"): 24,
            ("8", "9", "10", "Jack"): 28,
            ("9", "10", "Jack", "Queen"): 32,
            ("10", "Jack", "Queen", "King"): 36,
            ("Jack", "Queen", "King", "Ace"): 40
        }

        self.straight_five = {
            ("3", "4", "5", "6", "7"): 25,
            ("4", "5", "6", "7", "8"): 30,
            ("5", "6", "7", "8", "9"): 35,
            ("6", "7", "8", "9", "10"): 40,
            ("7", "8", "9", "10", "Jack"): 44,
            ("8", "9", "10", "Jack", "Queen"): 47,
            ("9", "10", "Jack", "Queen", "King"): 49,
            ("10", "Jack", "Queen", "King", "Ace"): 50
        }

        self.straight_six = {
            ("3", "4", "5", "6", "7", "8"): 33,
            ("4", "5", "6", "7", "8", "9"): 39,
            ("5", "6", "7", "8", "9", "10"): 45,
            ("6", "7", "8", "9", "10", "Jack"): 50,
            ("7", "8", "9", "10", "Jack", "Queen"): 54,
            ("8", "9", "10", "Jack", "Queen", "King"): 57,
            ("9", "10", "Jack", "Queen", "King", "Ace"): 59
        }

        self.straight_seven = {
            ("3", "4", "5", "6", "7", "8", "9"): 42,
            ("4", "5", "6", "7", "8", "9", "10"): 49,
            ("5", "6", "7", "8", "9", "10", "Jack"): 55,
            ("6", "7", "8", "9", "10", "Jack", "Queen"): 60,
            ("7", "8", "9", "10", "Jack", "Queen", "King"): 64,
            ("8", "9", "10", "Jack", "Queen", "King", "Ace"): 67
        }

        self.flush_three = {
            ("Hearts", "Hearts", "Hearts"): 0,
            ("Clubs", "Clubs", "Clubs"): 0,
            ("Spades", "Spades", "Spades"): 0,
            ("Diamonds", "Diamonds", "Diamonds"): 0
        }

        self.flush_four = {
            ("Hearts", "Hearts", "Hearts", "Hearts"): 0,
            ("Clubs", "Clubs", "Clubs", "Clubs"): 0,
            ("Spades", "Spades", "Spades", "Spades"): 0,
            ("Diamonds", "Diamonds", "Diamonds", "Diamonds"): 0
        }

        self.flush_five = {
            ("Hearts", "Hearts", "Hearts", "Hearts", "Hearts"): 0,
            ("Clubs", "Clubs", "Clubs", "Clubs", "Clubs"): 0,
            ("Spades", "Spades", "Spades", "Spades", "Spades"): 0,
            ("Diamonds", "Diamonds", "Diamonds", "Diamonds", "Diamonds"): 0
        }

        self.flush_six = {
            ("Hearts", "Hearts", "Hearts", "Hearts", "Hearts", "Hearts"): 0,
            ("Clubs", "Clubs", "Clubs", "Clubs", "Clubs", "Clubs"): 0,
            ("Spades", "Spades", "Spades", "Spades", "Spades", "Spades"): 0,
            ("Diamonds", "Diamonds", "Diamonds", "Diamonds", "Diamonds", "Diamonds"): 0
        }

        self.flush_seven = {
            ("Hearts", "Hearts", "Hearts", "Hearts", "Hearts", "Hearts", "Hearts"): 0,
            ("Clubs", "Clubs", "Clubs", "Clubs", "Clubs", "Clubs", "Clubs"): 0,
            ("Spades", "Spades", "Spades", "Spades", "Spades", "Spades", "Spades"): 0,
            ("Diamonds", "Diamonds", "Diamonds", "Diamonds", "Diamonds", "Diamonds", "Diamonds"): 0
        }
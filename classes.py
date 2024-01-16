from enum import Enum
from value_dictionary import *

class Faces(Enum):
    Ace = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine =  9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13

class Suits(Enum):
    Clubs = 1
    Hearts = 2
    Spades = 3
    Diamonds = 4

class Card:
    def __init__(self, face, suit, value):
        self.face = face
        self.suit = suit
        self.value = value

    def show_card(self):
        print(f'{self.face} of {self.suit}')


class Deck:
    def __init__(self):
        self.cards = []

    def create_deck(self):
        for suit in Suits:
            for face in Faces:
                self.cards.append(Card(face.name, suit.name, value_dictionary[face.name]))
    
    def get_deck(self):
        for card in self.cards:
            card.show_card()








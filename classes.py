
from enum import Enum
from value_dictionary import *
from collections.abc import Iterable  
from typing import Union

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
    def __init__(self, face:str, suit:str, value:int) -> None:
        self.face:str = face #face is type string
        self.suit:str = suit #suit is type string
        self.value:int = value #value is type int

    def show_card(self) -> None:
        print(f'{self.face} of {self.suit}')

class Hand:
    def __init__(self, player_name:str) -> None:
        self.hand:list[Card] = [] #hand is type list with object
        self.player_name = player_name #player name is type string
    

    def add_card(self, card:Card) -> None:
        self.hand.append(card)
        print(f'{self.player_name} got a {card}!')

    def count_hand(self) -> int:
        hand_value:int = 0
        for card in self.hand:
            hand_value += card.value
    
        if hand_value > 21:
            if self.has_ace():
                hand_value -= 10
                return hand_value
            
        return hand_value
        
        
    def has_ace(self) -> bool:
        for card in self.hand:
            if card.face == 'Ace':
                return True
        return False
    
    # def has_blackjack(self):
    #     if 

class Deck:
    def __init__(self) -> None:
        self.cards:list[Card] = [] #cards is type list

    def create_deck(self) -> None:
        for suit in Suits:
            for face in Faces:
                self.cards.append(Card(face.name, suit.name, value_dictionary[face.name]))
    
    def get_deck(self) -> None:
        for card in self.cards:
            card.show_card()

    def deal_card(self) -> None:
        self.cards.pop(0)

class Player:
    def __init__(self) -> None:
        pass

class Players:
    def __init__(self) -> None:
        self.players:list[object] = [] #players is type list


class DeckHalves:
    def __init__(self,left_half:list[Card], right_half:list[Card]) -> None:
        self.left_half:list[Card] = left_half
        self.right_half:list[Card] = right_half





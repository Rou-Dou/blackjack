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
    def __init__(self, face:str, suit:str, value:int) -> None:
        self.face:str = face #face is type string
        self.suit:str = suit #suit is type string
        self.value:int = value #value is type int

    def show_card(self) -> str:
        return f'{self.face} of {self.suit}'


class Hand:
    def __init__(self) -> None:
        self.hand:list[Card] = [] #hand is type list with object

    def add_card(self, card:Card) -> None:
        self.hand.append(card)

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
    
    def show_hand(self) -> str:
        card_position:int = 1
        hand_str:str = ''
        for card in self.hand:
            hand_str += (f'{card_position}: {card.show_card()}\n')
            card_position += 1
        return hand_str
    
    def get_dealer_up_card(self) -> Card:
        return self.hand[1]
    
    def clear_hand(self) -> None:
        self.hand.clear()
            

class Player:
    def __init__(self, type:str, player_name:str, money:int, hand:Hand) -> None:
        self.type:str = type
        self.player_name:str = player_name
        self.money:int = money
        self.hand:Hand = hand
    
    def get_player_hand(self) -> str:
        return f"{self.hand.show_hand()}"

class Deck:
    def __init__(self) -> None:
        self.cards:list[Card] = [] #cards is a list of class Card

    def create_deck(self) -> None:
        for suit in Suits:
            for face in Faces:
                self.cards.append(Card(face.name, suit.name, value_dictionary[face.name]))
    
    def get_deck(self) -> None:
        for card in self.cards:
            card.show_card()

    def deal_card(self) -> Card:
        return self.cards.pop(0)
    
    def burn_card(self) -> None:
        self.cards.pop(0)

    def append_deck(self, deck:list[Card]) -> None:
        self.cards = self.cards + deck

class DeckHalves:
    def __init__(self,left_half:list[Card], right_half:list[Card]) -> None:
        self.left_half:list[Card] = left_half 
        self.right_half:list[Card] = right_half
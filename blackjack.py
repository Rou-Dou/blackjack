from classes import *
from helpers import *

deck = Deck()

deck.create_deck()

deck.cards = shuffle_deck(deck.cards, 7)

deck.get_deck()
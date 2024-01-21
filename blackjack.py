from helpers import *
from entropy import *

# create deck object
deck = Deck()

# generate a fresh deck
deck.create_deck() #deck type is builtins.list

# save the fresh deck
fresh_deck = deck.cards #fresh_deck type is builtins.list

# shuffle the deck and store it in the deck object
deck.cards = shuffle_deck(deck.cards, 5) #deck.cards type is builtins.list

deck.get_deck()

print(f'entropy of shuffle is: {entropy_value(fresh_deck, deck.cards)}')

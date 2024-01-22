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

seat_positions:list = [1,2,3,4]
bot_names:list = ['Randy', 'John', 'Joe', 'Bobby', 'Jeoffry', 'Jinx', 'Jerome']

seat_position = getSeatPosition(seat_positions)

player_directory = Players()

createPlayer(player_directory, 'Matt', 100, seat_position)

while len(seat_positions) > 0:
    pop_index = randint(0, len(bot_names) - 1)
    seat_position = getSeatPosition(seat_positions)
    createPlayer(player_directory, bot_names.pop(pop_index), 100, seat_position)

# create dealer
createPlayer(player_directory, 'Dealer', 10000000, 5)

dealCards(deck, 5, player_directory)



from helpers import *
from entropy import *

# create deck object
deck = Deck()

turn = 1
num_turns = 4

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

while True:
    player_name = input('What is your name?: ')
    try: 
        first_player_hand = player_directory.get_player(player_name)
        break
    except:
        continue

print()
createPlayer(player_directory, player_name, 100, seat_position)

while len(seat_positions) > 0:
    pop_index = randint(0, len(bot_names) - 1)
    cpu_seat_position = getSeatPosition(seat_positions)
    createPlayer(player_directory, bot_names.pop(pop_index), 100, cpu_seat_position)

# create dealer
createPlayer(player_directory, 'Dealer', 10000000, 5)

dealCards(deck, 5, player_directory)



print(player_directory.dealer_face_up())
print()
print(player_directory.get_player(player_name).show_hand())

while True:
    if turn == seat_position:
        print(f'Current hand value is {player_directory.get_player(player_name).count_hand()}')
        player_hs = input('Would you like to hit or stand?: ')
    else:
        turn += 1

from helpers import *
from entropy import *
import mypy
import json

txt_file = open('player_dictionary.txt', 'r')
player_dictionary = json.load(txt_file)

turn:int = 1
num_turns:int = 4
deck:Deck = createNewDeck()
players:list[Player] = []
table:list[Player] = []
bot_names:list[str] = ['Randy', 'John', 'Joe', 'Bobby', 'Jeoffry', 'Jinx', 'Jerome']

# generate cpu and dealer
while len(bot_names) > 0:
    createPlayer(player_dictionary, 'cpu', bot_names.pop(0), 100)

createPlayer(player_dictionary, 'dealer', 'Dealer', 10000000)

cpus = len(player_dictionary['cpu'])

# create player character
player_name_prompt:str = 'What is your name?: '
while True:
    player_name:str = input(player_name_prompt)

    if player_name.lower() == 'dealer':
        player_name_prompt:str = 'Invalid player_name, please enter a different name: '
    elif hasNumbers(player_name):
        player_name_prompt:str = 'Please only include alphabetical characters in your name: '
    else:
        break

# create the player character
createPlayer(player_dictionary, 'player', player_name, 100)

players.append(player_dictionary['player'][0])

for i in range(0,3):
    players.append(player_dictionary['cpu'][randint(0, cpus - 1)])

#assign seats
for i in range(0,4):
    table.append(players.pop(randint(0,len(players)-1)))
table.append(player_dictionary['dealer'][0])


dealCards(deck, 5, table)

# first_player:Hand = player_directory.get_player_by_id()

# print(player_directory.get_player_by_id(dealer_id)
print()
# print(first_player.show_hand())

# Game Loop
while turn < 6:
    current_player = player_directory.get_player_by_seat(turn)
    dealer = player_directory.get_player_by_name('dealer')
    dealer_up_card = player_directory.get_dealer_up_card()
    
    # Hit/Stand loop
    while True:
        hand_value = current_player.count_hand()
        
        # first_player turn
        if current_player.player_name == first_player.player_name:
            print(f'Current hand value is {first_player.count_hand()}\n')

            player_hs:str = input('Would you like to hit or stand?: ')

            if player_hs.lower() == 'hit':
                dealt_card = deck.deal_card()
                first_player.add_card(dealt_card)
                print(f'you got a {dealt_card.show_card()}')

                if current_player.count_hand() > 21:
                    print(f'You busted!')
                    break
            
                print(f'{current_player.show_hand()} value: {current_player.count_hand()}\n')

            elif player_hs.lower() == 'stand':
                print(f'You stood with a hand of: {first_player.show_hand()} with a value of {first_player.count_hand()}\n')
                break
            
        # CPU turn
        elif current_player.id != dealer_id:
            print(f'{current_player.show_hand()} value: {current_player.count_hand()}\n')
            
            shouldHit:bool = False

            if current_player.count_hand() > 21:
                print(f'{current_player.player_name} Busted!\n')
                break

            if dealer_up_card >= 7 and 12 <= hand_value <= 16:
                shouldHit = True
            elif 1 < dealer_up_card < 4 and hand_value == 12:
                shouldHit = True
            elif dealer_up_card > 9 and hand_value == 10:
                shouldHit = True
            elif dealer_up_card == 2 or dealer_up_card >= 7 and hand_value == 9:
                shouldHit = True
            elif hand_value == 8:
                shouldHit = True

            if shouldHit:
                dealt_card = deck.deal_card()
                current_player.add_card(dealt_card)
                print(f'{current_player.player_name} Hit\nThey received a {dealt_card.show_card()}\n')

            else:
                print(f'{current_player.player_name} Stood\n')
                break
        
        # Dealer Turn
        else:
            print(f'{dealer.show_hand()}\nValue: {dealer.count_hand()}') 
            dealer_hand_value = dealer.count_hand()
            
            if dealer_hand_value > 21:
                print('The dealer busted!')
                break

            elif dealer_hand_value < 17:
                dealt_card = deck.deal_card()
                dealer.add_card(dealt_card)
                print(f'The dealer hit\nValue: {dealer.count_hand()}\n They got a {dealt_card.show_card()}')
            
            else:
                print(f'The dealer stood with a hand value of {dealer.count_hand()}\n')
                break
        
            
        if len(deck.cards) < 5:
            new_deck = createNewDeck()
            deck.append_deck(new_deck.cards)

    turn += 1


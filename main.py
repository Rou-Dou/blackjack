from helpers import *
from entropy import *
import mypy
import json
from time import sleep

txt_file = open('player_dictionary.json', 'r')
player_dictionary = json.load(txt_file)
bot_txt = open('bot_names.txt', 'r')
bot_names = []
for line in bot_txt:
    bot_names.append(line.strip())
txt_file.close()

turn:int = 1
num_turns:int = 4
deck:Deck = createNewDeck()
players:list[Player] = []
table:list[Player] = []

# generate cpu and dealer
while len(bot_names) > 0:
    createPlayer(player_dictionary, 'cpu', bot_names.pop(0), 100)

createPlayer(player_dictionary, 'dealer', 'Dealer', 10000000)

save_info = json.dumps(player_dictionary, indent=4)

with open('player_dictionary.txt', 'w') as json_file:
    json_file.write(save_info)

cpus = len(player_dictionary['cpu'])

# create player character
player_name_prompt:str = 'What is your name?: '

while True:
    player_name:str = input(player_name_prompt)

    if player_name.lower() == 'dealer':
        player_name_prompt:str = 'Invalid player_name, please enter a different name: \n'
    elif hasNumbers(player_name):
        player_name_prompt:str = 'Please only include alphabetical characters in your name: \n'
    else:
        break

# create the player character
first_player_id = createPlayer(player_dictionary, 'player', player_name, 100)

players.append(player_dictionary['player'][first_player_id])

while len(players) < 4:
    selected_player = player_dictionary['cpu'][randint(0, cpus - 1)]
    if not selected_player in players:
        players.append(selected_player)

#assign seats
for i in range(0,4):
    table.append(players.pop(randint(0,len(players)-1)))
table.append(player_dictionary['dealer'][0])

dealCards(deck, 5, table)

dealer_up_card = table[4].hand.get_dealer_up_card()
dealer_up_card_value = dealer_up_card.value

print(f"\nThe dealer has a {dealer_up_card.show_card()}")
# Hit/Stand loop
for player in table:
    print(f"\n{player.player_name}'s turn: \n")
    while True:
        # first_player turn
        if player.type == 'player':
            print(f'Current hand value is {player.hand.count_hand()}\n')

            player_hs:str = input('Would you like to hit or stand?: ')

            if player_hs.lower() == 'hit':
                dealt_card = deck.deal_card()
                player.hand.add_card(dealt_card)
                print(f'you got a {dealt_card.show_card()}')

                if player.hand.count_hand() > 21:
                    print(f'You busted!')
                    break
            
                print(f'{player.get_player_hand()} value: {player.hand.count_hand()}\n')

            elif player_hs.lower() == 'stand':
                print(f'You stood with a hand of:\n {player.get_player_hand()} with a value of {player.hand.count_hand()}\n')
                break
            
        # CPU turn
        elif player.type == 'cpu':
            print(f'{player.hand.show_hand()} value: {player.hand.count_hand()}\n')
            
            shouldHit:bool = False

            hand_value = player.hand.count_hand()

            if hand_value > 21:
                print(f'{player.player_name} Busted!\n')
                break
            print('Thinking.')
            sleep(1)
            print('Thinking..')
            sleep(1)
            print('Thinking...\n')
            sleep(1)
            if dealer_up_card_value >= 7 and 12 <= hand_value <= 16:
                shouldHit = True
            elif 1 < dealer_up_card_value < 4 and hand_value == 12:
                shouldHit = True
            elif dealer_up_card_value > 9 and hand_value == 10:
                shouldHit = True
            elif dealer_up_card_value == 2 or dealer_up_card_value >= 7 and hand_value == 9:
                shouldHit = True
            elif hand_value == 8:
                shouldHit = True

            if shouldHit:
                dealt_card = deck.deal_card()
                player.hand.add_card(dealt_card)
                print(f'{player.player_name} Hit\nThey received a {dealt_card.show_card()}\n')

            else:
                print(f'{player.player_name} Stood\n')
                break
        
        # Dealer Turn
        else:
            dealer_hand_value = player.hand.count_hand()            
            print(f'{player.hand.show_hand()}\nValue: {dealer_hand_value}') 
            
            if dealer_hand_value > 21:
                print('The dealer busted!')
                break

            elif dealer_hand_value < 17:
                dealt_card = deck.deal_card()
                player.hand.add_card(dealt_card)
                print(f'The dealer hit\nThey got a {dealt_card.show_card()}\nValue: {player.hand.count_hand()}')
            
            else:
                print(f'The dealer stood with a hand value of {player.hand.count_hand()}\n')
                break
        
            
        if len(deck.cards) < 5:
            new_deck = createNewDeck()
            deck.append_deck(new_deck.cards)


for player in table:
    player.hand.clear_hand()


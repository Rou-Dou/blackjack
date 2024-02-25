from helpers import *
from entropy import *
import mypy
from time import sleep

player_dictionary = init_game()

turn:int = 1
num_turns:int = 4
deck:Deck = createNewDeck()
players:list[Player] = []
table:list[Player] = []

cpus = len(player_dictionary['cpu'])

# create player character
player_name_prompt:str = 'What is your players name?: '

while True:
    player_name:str = input(player_name_prompt)

    if player_name.lower() == 'dealer':
        player_name_prompt:str = 'Invalid player_name, please enter a different name: \n'
    elif hasNumbers(player_name):
        player_name_prompt:str = 'Please only include alphabetical characters in your name: \n'
    else:
        break

players.append(createPlayer(player_dictionary, 'player', player_name, 100))


while len(players) < 4:
    selected_player = player_dictionary['cpu'][randint(0, cpus - 1)]
    if not selected_player in players:
        players.append(Player('cpu', selected_player["player_name"], selected_player["money"], Hand()))

#assign seats
for i in range(0,4):
    table.append(players.pop(randint(0,len(players)-1)))
dealer = player_dictionary['dealer'][0]
table.append(Player('dealer', dealer['player_name'], dealer['money'], Hand()))

dealCards(deck, 5, table)

dealer_up_card = table[4].hand.get_dealer_up_card()
dealer_up_card_value = dealer_up_card.value

print(f"The dealer has a {dealer_up_card.show_card()}\n")
# Hit/Stand loop
for player in table:
    print(f"{player.player_name}'s turn: \n")
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


from helpers import *
from entropy import entropy_value, n
import mypy
from time import sleep

player_dictionary = init_game()

main_casino = Casino()
num_tables = 4
bet:int = 0
deck:Deck = createNewDeck()
    
dealer:Player = createPlayer(player_dictionary, 'dealer', player_dictionary['dealer'][0]["player_name"], player_dictionary['dealer'][0]['money'])

# create player character
player_name_prompt:str = 'What is your players name?: '

while True:
    player_name:str = input(player_name_prompt)

    if player_name.lower() == dealer.player_name.lower():
        player_name_prompt = 'Invalid player_name, please enter a different name: \n'
    elif hasNumbers(player_name):
        player_name_prompt = 'Please only include alphabetical characters in your name: \n'
    else:
        break

selected_profile:Player = createPlayer(player_dictionary, 'player', player_name, 2000)

# Populate the tables in the casino with players
for i in range(0, num_tables):
    populated_table:Table = populate_table(Table(), player_dictionary)
    if populated_table.getNumOpenSeats() > 0:
        main_casino.addTable(populated_table)

iterator:int = 1

for table in main_casino.tables:
    print(f'There are {table.getNumOpenSeats()} seat(s) available at table {iterator}:\n')
    print(f'currently at table {iterator}:\n')
    table.getTablePlayers()
    iterator += 1

while True:
    table_number:int = int(input('Which table would you like to check out? '))
    
    if table_number <= len(main_casino.tables) and table_number > 0 :
        selected_table  = main_casino.getTable(table_number)
        break

available_seats = selected_table.getOpenSeats()


seat_num:int = 1
for seat in available_seats:
    print(f'{seat_num-1}: seat {seat + 1}')
    seat_num += 1

while True:
    seat_selected:int = int(input('Which seat would you like to sit at?: '))

    if seat_selected < len(available_seats) and seat_selected > -1:
        selected_table.table_seats[available_seats[seat_selected]] = selected_profile
        break

while True:
    for player in selected_table.table_seats:
        if player.type == '':
            continue

        elif player.type == 'cpu':
            dice_roll:int = randint(1,6)
            reroll:int = randint(1,6)
            matches:int = 0
            while reroll == dice_roll:
                reroll = randint(1,6)
                matches += 1
            if matches == 0:
                player.makeBet(randint(10,20))
            elif matches == 1:
                player.makeBet(randint(15,25))
            elif matches == 2:
                player.makeBet(randint(25,40))
            elif matches > 2:
                player.makeBet(randint(40, 100))
            print(f'{player.player_name} bet {player.bet} chips')
        
        elif player.type == 'player':
            bet = player_bet_input(player)
            player.makeBet(bet)
            print(f'You bet {player.bet} chips')

    table = selected_table.table_seats

    dealCards(deck, table)

    dealer_up_card = table[4].hand.get_dealer_up_card()
    dealer_up_card_value = dealer_up_card.value

    print(f"The dealer has a {dealer_up_card.show_card()}\n")
    # Hit/Stand loop
    for player in table:
        if player.type == '':
            continue
        print(f"{player.player_name}'s turn: \n")
        while True:
            # first_player turn
            if player.type == 'player':
                print(player.hand.show_hand())
                print(f'Current hand value is {player.hand.count_hand()}\n')

                player_hs:str = input('What would you like to do? (hit/stand/double down/split): ')

                if player_hs.lower() == 'double down' or player_hs.lower() == 'doubledown':
                    player.bet = player.bet*2
                    print(f'Your current bet is now {player.bet} chips')
                    dealt_card = deck.deal_card()
                    player.hand.add_card(dealt_card)
                    print(f'you got a {dealt_card.show_card()}')
                    checkPlayerBust(player)
                    print(f'{player.get_player_hand()} value: {player.hand.count_hand()}\n')
                    sleep(1)
                    break

                elif player_hs.lower() == 'hit':
                    dealt_card = deck.deal_card()
                    player.hand.add_card(dealt_card)
                    print(f'you got a {dealt_card.show_card()}')
                    print(f'{player.get_player_hand()} value: {player.hand.count_hand()}\n')
                                        
                    if checkPlayerBust(player):
                        break

                elif player_hs.lower() == 'stand':
                    print(f'You stood with a hand of:\n{player.get_player_hand()} with a value of {player.hand.count_hand()}\n')
                    player.setStatus(False)
                    break

                
            # CPU turn
            elif player.type == 'cpu':
                print(f'{player.hand.show_hand()} value: {player.hand.count_hand()}\n')
                
                shouldHit:bool = False

                hand_value = player.hand.count_hand()

                if hand_value > 21:
                    print(f'{player.player_name} Busted!\n')
                    player.money -= player.bet
                    player.setStatus(True)
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
                    player.setStatus(False)
                    break
            
            # Dealer Turn
            else:
                dealer_hand_value = player.hand.count_hand()            
                print(f'{player.hand.show_hand()}\nValue: {dealer_hand_value}') 
                
                if dealer_hand_value > 21:
                    print('The dealer busted!')
                    player.setStatus(True)
                    break

                elif dealer_hand_value < 17:
                    dealt_card = deck.deal_card()
                    player.hand.add_card(dealt_card)
                    print(f'The dealer hit\nThey got a {dealt_card.show_card()}\nValue: {player.hand.count_hand()}')
                
                else:
                    print(f'The dealer stood with a hand value of {player.hand.count_hand()}\n')
                    player.setStatus(False)
                    break
            
                
            if len(deck.cards) < 10:
                new_deck = createNewDeck()
                deck.append_deck(new_deck.cards)

    dealer_info:Player = selected_table.table_seats.pop(4)

    for player in table:
        if player.type == '' or player.type == 'dealer':
            continue

        elif (dealer_info.over == True and player.over == False) or \
        (player.hand.count_hand() > dealer_hand_value and player.over == False):
            player.money += round(player.bet * 1.5)

        elif player.hand.count_hand() < dealer_hand_value and player.over == False:
            player.money -= round(player.bet)

        print(f"{player.player_name} has {player.money} chips")

    # reset game
    print()
    resetTable(selected_table, player_dictionary)

    # ask for quit
    play_again:str = ''
    while play_again.lower() != 'no' and play_again != 'yes':
        play_again = input('Would you like to play another round (yes/no)? ')
    
    if play_again == 'no':
        break
    








from helpers import *
from typing import Any
from random import randint
import mypy
from time import sleep

# main globals
player_dictionary: dict[str, Any] = initGame()
main_casino: Casino = Casino()
num_tables: int = 4
bet: int = 0
deck: Deck = createNewDeck()
dealer: Player = Player('dealer', player_dictionary['dealer'][0]["player_name"], player_dictionary['dealer'][0]['money'], player_dictionary['dealer'][0]['affinity'])

# Player character select. Print current players and prompt for selection
# If the player types 'new' create a new character, otherwise
# store the selected index value, then create the Player class
while True:
    for count, player in enumerate(player_dictionary['player']):
        print(f'{count+1}: {player["player_name"]}')

    profile_index: str = input('Type the number of the profile you would like to use? Type "new" to create a new profile: ' )

    if (profile_index not in '0123456789' and profile_index != 'new') \
        or (int(profile_index) > len(player_dictionary['player']) or int(profile_index) < 1):
        
        continue

    if profile_index == 'new':
        createPlayerCharacter(player_dictionary)
    else:
        profile_index_int: int = int(profile_index)
        break

profile_object = player_dictionary["player"][profile_index_int - 1]
selected_profile = Player('player', profile_object['player_name'], profile_object["money"], profile_object['affinity'])

# Populate the tables in the casino with players
for i in range(0, num_tables):
    populated_table: Table = populate_table(Table(), player_dictionary)
    if populated_table.getNumOpenSeats() > 0:
        main_casino.addTable(populated_table)

# display the current population of tables and the players at them
for count, table in enumerate(main_casino.tables):
    print()
    table.printTablePlayers(count)

# prompt for table to sit at
while True:
    try:
        table_number: int = int(input('Which table would you like to check out? '))
    except:
        print('Please enter a valid number from the provided list')
        continue

    if table_number <= len(main_casino.tables) and table_number > 0:
        selected_table  = main_casino.getTable(table_number)
        break

# print seats available at the chose table
available_seats = selected_table.getOpenSeats()

for seat in available_seats:
    print(f'{seat + 1}: seat {seat + 1}')

# prompt player for preferred seat
while True:
    seat_selected: int = int(input('Which seat would you like to sit at?: '))

    if seat_selected <= len(available_seats) and seat_selected > 0:
        selected_table.table_seats[available_seats[seat_selected-1]] = selected_profile
        break

# Betting loop
while True:
    for player in selected_table.table_seats:
        if player.type == '':
            continue
        
        # CPU loop, based on dice rolls, the CPU bets more or less.
        elif player.type == 'cpu':
            dice_roll: int = randint(1,6)
            reroll: int = randint(1,6)
            matches: int = 0
            while reroll == dice_roll:
                reroll = randint(1,6)
                matches += 1
            match matches:
                case 0:
                    player.makeBet(randint(10,50))
                case 1:
                    player.makeBet(randint(50,100))
                case 2: 
                    player.makeBet(randint(100,200))
                case _:
                    player.makeBet(randint(200, 1000))
            
            print(f'{player.player_name} bet {player.bet} chips')
        
        # Player is prompted to bet here
        elif player.type == 'player':
            bet = player_bet_input(player)
            player.makeBet(bet)
            typeWriter(f'You bet {player.bet} chips')

    table_players: list[Player] = selected_table.table_seats

    # give each player at the table a hand and deal cards
    for player in table_players:
        player.createHand()
    
    dealCards(deck, table_players)

    # Print dealer information for player
    dealer_up_card = table_players[4].hands[0].get_dealer_up_card()
    dealer_up_card_value = dealer_up_card.value

    print(f"The dealer has a {dealer_up_card.show_card()}\n")

    ### Hit/Stand loop ###

    # Empty player seats are skipped, search for player type to determine what to do
    for player in table_players:
        if player.type == '':
            continue
        print(f"{player.player_name}'s turn: \n")
        for hand in player.hands:
            while True:
                # first_player turn
                if player.type == 'player':
                    hand.print_hand()
                    print(f'Current hand value is {hand.count_hand()}\n')
                    
                    if player.hasTwentyOne(hand):
                        break

                    # prompt player for their action, logic will catch their decision
                    player_hs: str = input('What would you like to do? (hit/stand/double down/split): ').lower()

                    # in the case of double down, the player's bet is doubled and they are dealt a new card
                    # If they bust the hand is resolved right away, otherwise they are forced to stand
                    if player_hs == 'double down' or player_hs == 'doubledown':
                        player.bet = player.bet*2
                        print(f'Your current bet is now {player.bet} chips')
                        deck.deal_card(hand)
                        checkPlayerBust(player)
                        print(f'{player.print_player_hand()} value: {hand.count_hand()}\n')
                        sleep(1)
                        break
                    
                    # In the case that 'split' is selected, the first the case is checked
                    # if it is a valid split situation, the player is given an additional hand, their
                    # original hand is split, and they proceed to play both hands.
                    elif player_hs == 'split':
                        if len(hand.cards) == 2:
                            if hand.cards[0].face == hand.cards[1].face:
                                new_hand = Hand()
                                new_hand.add_card(hand.cards.pop(1))
                                player.hands.append(new_hand)
                                
                                for hand in player.hands:
                                    deck.deal_card(hand)
                                
                                
                    # if the player hits, they are dealt a new card and are checked for a bust.
                    elif player_hs == 'hit':
                        dealt_card: Card = deck.deal_card(hand)
                        typeWriter(f'The dealer dealt a {dealt_card.face} of {dealt_card.suit}')
                    
                                            
                        if checkPlayerBust(player):
                            break

                    # if the player stands their hand is printed and the loop is broken.
                    elif player_hs == 'stand':
                        print(f'You stood with a hand of: ')
                        player.print_player_hand()
                        print(f'with a value of {hand.count_hand()}\n')
                        player.setStatus(False)
                        break

                
                # CPU turn
                elif player.type == 'cpu':
                    shouldHit: bool = False
                    hand_value: int = hand.count_hand()

                    if checkPlayerBust(player) or player.hasTwentyOne(hand):
                        break

                    # logic here is based on 'ideal' blackjack play at a basic level
                    # A simple series of dealer/player conditions are considered for when the CPU
                    # should hit, otherwise `shouldHit` is false by default and the CPU will stand.
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
                        deck.deal_card(hand)
                    # stand
                    else:
                        player.setStatus(False)
                        break
                
                # Dealer Turn
                else:
                    dealer_hand_value: int = hand.count_hand()            
                    hand.print_hand()
                    print(f'\nValue: {dealer_hand_value}')

                    if checkPlayerBust(player) or player.hasTwentyOne(hand):
                        break

                    elif dealer_hand_value < 17:
                        deck.deal_card(hand)
                                            
                    else:
                        print(f'The dealer stood with a hand value of {hand.count_hand()}\n')
                        player.setStatus(False)
                        break

            # check if a new deck needs to be created and create one if so    
            if len(deck.cards) < 10:
                new_deck: Deck = createNewDeck()
                deck.append_deck(new_deck.cards)

    # remove the dealer from the table and store his final hand values
    dealer_info: Player = selected_table.table_seats.pop(4)
    dealer_hand_value: int = dealer_info.hands[0].count_hand()

    #### Payout/loss calculation ####
    # for each player or CPU type, check a series of conditions and add or subtract chips 
    for player in table_players:
        if player.type == '' or player.type == 'dealer':
            continue
        
        # for each hand, check if the player has beaten the dealer, give them 2 to 1 payout, 
        # otherwise subtract chips. The loss calculations are only if the player has not gone over 21
        # over 21 calculations are calculated at the time of the bust
        for hand in player.hands:
            if (player.over == False and (dealer_info.over == True or hand.count_hand() > dealer_hand_value)):
                player.money += round(player.bet * 1.5)

            elif hand.count_hand() < dealer_hand_value and player.over == False:
                player.money -= round(player.bet)

        print(f"{player.player_name} has {player.money} chips")
        index: int = findPlayer(player_dictionary, player)
        player_dictionary[player.type][index]["money"] = player.money

    # reset game
    print()
    resetTable(selected_table, player_dictionary)
    saveGame(player_dictionary)

    # ask for quit
    play_again: str = ''
    while play_again != 'no' and play_again != 'yes':
        try:
            play_again = input('Would you like to play another round (yes/no)? ').lower()
        except:
            print('Invalid Input')
    
    if play_again == 'no':
        break
    








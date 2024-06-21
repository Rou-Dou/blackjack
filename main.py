from helpers import *
import mypy

# main globals
min_bets: list[int] = [10, 25, 50, 100]
num_tables: int = 4
main_casino: Casino = Casino(num_tables)
selected_seat: int = -1
selected_profile: Player
dealer: Dealer


# Player character select. Print current players and prompt for selection
# If the player types 'new' create a new character, otherwise
# store the selected index value, then create the Player class
while True:
    for count, player in enumerate(player_dictionary['player'], 1):
        print(f'{count}: {player["player_name"]}')

    profile_index: str = input(prompts["profile"])

    if profile_index == 'new':
        createPlayerCharacter(player_dictionary)

    elif not profile_index.isdigit() or ( \
        int(profile_index) > len(player_dictionary['player']) or \
        int(profile_index) < 1):
        continue

    else:
        profile_index_int: int = int(profile_index)
        break

profile_object = player_dictionary["player"][profile_index_int - 1]
selected_profile = Player(profile_object['player_id'], 'player', profile_object['player_name'], profile_object["money"], profile_object['affinity'])

# Populate the tables in the casino with players
for i in range(0, num_tables):
    new_dealer: Dealer = Dealer('', Deck(), Hand())
    new_table: Table = Table(new_dealer, min_bets[i])
    new_table._populateTable()
    main_casino.addTable(new_table)

# display the current population of tables and the players at them
for count, table in enumerate(main_casino.tables):
    if not table.hasOpenSeats():
        print(f'table {count+1} is full')
        continue
    print(f'\nminimum bet for this table is {table.minimum_bet}')
    table.printTablePlayers(count)

# prompt for table to sit at1

while True:
    try:
        table_number: int = int(input(prompts["table"]))
    except Exception:
        print(prompts["invalid_list_input"])
        continue

    if table_number <= len(main_casino.tables) and table_number > 0:
        selected_table  = main_casino.getTable(table_number)
        if selected_table.hasOpenSeats():
            break
        else:
            print(f'Table {table_number} is full, please choose a table with open seats.')
    


# print seats available at the chose table
dealer = selected_table.dealer
available_seats = selected_table.getOpenSeats()

for seat in available_seats:
    seat += 1
    print(f'seat {seat}')

# prompt player for preferred seat
while True:
    try:
        selected_seat = int(input(prompts["seat"]))
    except Exception: 
        print('invalid input, please enter a valid seat number')

    if  selected_seat > 0 and (selected_seat - 1) in available_seats:
        selected_table.table_seats[selected_seat-1] = selected_profile
        break

# Betting loop
while True:
    for player in selected_table.table_seats:
        if player == None:
            continue
        
        # CPU loop, based on dice rolls, the CPU bets more or less.
        elif player.type == 'cpu':
            player.makeBet(0, selected_table.minimum_bet)
            print(f'{player.player_name} bet {player.bet} chips')
        
        # Player is prompted to bet here
        elif player.type == 'player':
            bet: int = player_bet_input(player)
            player.makeBet(bet, selected_table.minimum_bet)
            typeWriter(f'You bet {player.bet} chips')

    table_players: list[Union[Player, None]] = selected_table.table_seats

    # give each player at the table a hand and deal cards
    for player in table_players:
        if player is not None:
            player.createHand()

    table.dealer.createHand()
    
    dealCards(dealer, table_players)

    # Print dealer information for player
    dealer_up_card: Card = dealer.get_dealer_up_card()
    dealer_up_card_value: int = dealer_up_card.value
    deck = table.dealer.deck

    print(f"The dealer has a {dealer_up_card.show_card()}\n")

    ### Hit/Stand loop ###

    # Empty player seats are skipped, search for player type to determine what to do
    for player in table_players:

        if player is None:
            continue

        # check if a new deck needs to be created and create one if so    
        if deck.num_cards() < 15:
            new_deck: Deck = Deck()
            deck.append_deck(new_deck)

        for hand in player.hands:
            while True:
                # first_player turn
                if player.type == 'player':
                    player.print_player_hand()
                    
                    if player.hasTwentyOne(hand):
                        break

                    # prompt player for their action, logic will catch their decision]
                    player_prompt: str = 'What would you like to do? (hit/stand/double down/split): '
                    player_response: str = player_input(player_prompt, ['hit', 'stand', 'doubledown', 'double down', 'split'])

                    # in the case of double down, the player's bet is doubled and they are dealt a new card
                    # If they bust the hand is resolved right away, otherwise they are forced to stand
                    if player_response == 'double down' or player_response == 'doubledown':
                        player.bet = player.bet*2
                        print(f'Your current bet is now {player.bet} chips')
                        dealer.deal_card(hand)
                        player.isOver()
                        player.print_player_hand()
                        sleep(1)
                        break
                    
                    # In the case that 'split' is selected, the first the case is checked
                    # if it is a valid split situation, the player is given an additional hand, their
                    # original hand is split, and they proceed to play both hands.
                    elif player_response == 'split':
                        if len(hand.cards) == 2:
                            if hand.cards[0].face == hand.cards[1].face:
                                new_hand = Hand()
                                new_hand.add_card(hand.cards.pop(1))
                                player.hands.append(new_hand)
                                
                                for hand in player.hands:
                                    dealer.deal_card(hand)
                                
                    # if the player hits, they are dealt a new card and are checked for a bust.
                    elif player_response == 'hit':
                        dealt_card: Card = dealer.deal_card(hand)
                        typeWriter(f'The dealer dealt a {dealt_card.face} of {dealt_card.suit}')
                              
                        if player.isOver():
                            break

                    # if the player stands their hand is printed and the loop is broken.
                    elif player_response == 'stand':
                        print('You stood')
                        player.print_player_hand()
                        player.setStatus(False)
                        break

                
                # CPU turn
                elif player.type == 'cpu':
                    hand_value: int = hand.count_hand()
                    willHit: bool = shouldHit(dealer_up_card_value, hand_value)

                    # bust 
                    if player.isOver():
                        break

                    # 21/blackjack
                    elif player.hasTwentyOne(hand):
                        break
                    
                    # hit
                    elif willHit:
                        dealer.deal_card(hand)

                    # stand
                    else:
                        print(f'{player.player_name} stood')
                        player.setStatus(False)
                        break

                
    # Dealer Turn
    print("\nDealers Turn")
    while True:
        dealer_hand_value: int = dealer.hands[0].count_hand()      
        dealer.hands[0].print_hand()
        print(f'\nValue: {dealer_hand_value}')

        if dealer.isOver() or dealer.hasTwentyOne(hand):
            break

        elif dealer_hand_value < 17:
            new_card = dealer.deal_card(dealer.hands[0])
            print(f'The dealer got a {new_card.show_card()}')
        else:
            print(f'The dealer stood with a hand value of {dealer_hand_value}\n')
            dealer.setStatus(False)
            break

    # store dealer hand values for evaluation
    dealer_hand_value = dealer.hands[0].count_hand()

    #### Payout/loss calculation ####
    # for each player or CPU type, check a series of conditions and add or subtract chips 
    for player in table_players:
        if player is None:
            continue
        
        # for each hand, check if the player has beaten the dealer, give them 2 to 1 payout, 
        # otherwise subtract chips. The loss calculations are only if the player has not gone over 21
        # over 21 calculations are calculated at the time of the bust
        for hand in player.hands:
            if (not player.over and (dealer.over or hand.count_hand() > dealer_hand_value)):
                player.money += round(player.bet * 1.5)

            elif hand.count_hand() < dealer_hand_value and not player.over:
                player.money -= round(player.bet)

        print(f"{player.player_name} has {player.money} chips")
        index: int = findPlayer(player_dictionary, player)
        player_dictionary[player.type][index]["money"] = player.money

    # reset game
    print()
    selected_table.resetTable()
    saveGame(player_dictionary)

    # ask for quit
    player_prompt = 'Would you like to play another round (yes/no)? '
    player_response = player_input(player_prompt, ['yes', 'no'])
    
    if player_response == 'no':
        break
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

    player_prompt = prompts_responses["prompts"]["profile"]

    profile_index: str = input(player_prompt)

    if profile_index == 'new':
        createPlayerCharacter()

    elif not profile_index.isdigit() \
        or (int(profile_index) > len(player_dictionary['player']) \
        or  int(profile_index) < 1):
        continue

    else:
        profile_index_int: int = int(profile_index)
        break


profile_object: dict = player_dictionary["player"][profile_index_int - 1]
selected_profile = Player(profile_object['player_id'], 
                         'player', profile_object['player_name'], 
                          profile_object["money"], 
                          profile_object['affinity']
                         )

print()

# Populate the tables in the casino with players
for i in range(0, num_tables):
    new_dealer: Dealer = Dealer('', Deck(), Hand())
    new_table: Table = Table(new_dealer, min_bets[i])
    new_table.populate_table()
    main_casino.add_table(new_table)


# display the current population of tables and the players at them
typeWriter(main_casino, 'fast')

# prompt for table to sit at
while True:
    player_prompt = prompts_responses["prompts"]["table"]
    try:
        table_number: int = int(input(player_prompt))
    except Exception:
        print(prompts_responses["errors"]["invalid_list_input"])
        continue

    if table_number <= len(main_casino.tables) and table_number > 0:
        selected_table  = main_casino.get_table(table_number)
        if selected_table.has_open_seats():
            break
        else:
            typeWriter(f'Table {table_number} is full, please choose a table with open seats.')


# print seats available at the chose table
dealer = selected_table.dealer
available_seats = selected_table.get_open_seats()

for seat in available_seats:
    print(f'seat {seat + 1}')


# prompt player for preferred seat
while True:
    player_prompt = prompts_responses["prompts"]["seat"]
    try:
        selected_seat = int(input(player_prompt))
    except Exception:
        error_prompt = player_prompt["errors"]["invalid_seat_num"]
        print(error_prompt)

    if  selected_seat > 0 and (selected_seat - 1) in available_seats:
        selected_table.table_seats[selected_seat-1] = selected_profile
        break


#### Main game loop ####
while True:

    ## betting ##
    for player in selected_table.table_seats:
        if player is None:
            continue
        
        # CPU loop, based on dice rolls, the CPU bets more or less.
        elif not player.is_player():
            player.make_bet(0, selected_table.minimum_bet)
            print(f'{player.player_name} bet {player.bet} chips')
        
        # Player is prompted to bet here
        elif player.is_player():
            bet: int = playerBetInput(player)
            player.make_bet(bet, selected_table.minimum_bet)
            typeWriter(f'You bet {player.bet} chips')

    selected_table.initiate_hand()

    # Print dealer information for player
    dealer_up_card: Card = dealer.get_dealer_up_card()
    dealer_up_card_value: int = dealer_up_card.value
    deck = selected_table.dealer.deck

    typeWriter(f"The dealer has a {dealer_up_card.show_card()}\n")

    ### Hit/Stand loop ###

    # Empty player seats are skipped, search for player type to determine what to do
    for player in selected_table.table_seats:

        if player is None:
            continue

        # check if a new deck needs to be created and create one if so    
        if deck.is_thin():
            new_deck: Deck = Deck()
            deck.append_deck(new_deck)

        for hand in player.hands:
            while True:
                # first_player turn
                if player.is_player():
                    typeWriter(hand, 'fast')
                    
                    if player.has_twenty_one(hand):
                        break

                    # prompt player for their action, logic will catch their decision
                    valid_player_actions: list[str] = ['hit', 'stand', 'doubledown', 'split']
                    
                    player_prompt = prompts_responses["prompts"]["hand_decision"]

                    player_response: str = playerInput(
                        player_prompt, 
                        valid_player_actions
                    )

                    # in the case of double down, the player's bet is doubled and they are dealt a new card
                    # If they bust the hand is resolved right away, otherwise they are forced to stand
                    if player_response == 'doubledown':
                        player.bet = player.bet*2
                        typeWriter(f'Your current bet is now {player.bet} chips')

                        dealer.deal_card(hand)

                        player.has_busted()

                        print(hand)
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
                              
                        if player.has_busted():
                            break

                    # if the player stands their hand is printed and the loop is broken.
                    elif player_response == 'stand':
                        typeWriter(f'You stood \n\n{hand}', 'fast')
                        break

                
                # CPU turn
                elif  not player.is_player():
                    hand_value: int = hand.value
                    willHit: bool = shouldHit(dealer_up_card_value, hand_value)

                    # bust 
                    if player.has_busted():
                        break

                    # 21/blackjack
                    elif player.has_twenty_one(hand):
                        break
                    
                    # hit
                    elif willHit:
                        dealer.deal_card(hand)

                    # stand
                    else:
                        print(f'{player.player_name} stood', end='\n\n')
                        break

                
    # Dealer Turn
    print("Dealers Turn", end='\n\n')
    while True:
        dealer_hand: Hand = dealer.hands[0]
        dealer_hand_value: int = dealer_hand.value
        print(dealer_hand)

        if dealer.has_busted() or dealer.has_twenty_one(dealer_hand):
            break

        elif dealer_hand_value < 17:
            new_card = dealer.deal_card(dealer.hands[0])
            print(f'The dealer got a {new_card.show_card()}')
        else:
            print(f'The dealer stood with a hand value of {dealer_hand_value}', end='\n\n')
            break

    # store dealer hand values for evaluation
    dealer_hand_value = dealer.hands[0].value

    #### Payout/loss calculation ####
    # for each player or CPU type, check a series of conditions and add or subtract chips 
    for player in selected_table.table_seats:
        if player is None:
            continue
        
        # for each hand, check if the player has beaten the dealer, give them 2 to 1 payout, 
        # otherwise subtract chips. The loss calculations are only if the player has not gone over 21
        # over 21 calculations are calculated at the time of the bust
        for hand in player.hands:
            if (not player.over and (dealer.over or hand.value > dealer_hand_value)):
                player.money += round(player.bet * 1.5)

            elif hand.value < dealer_hand_value and not player.over:
                player.money -= round(player.bet)

        print(f"{player.player_name} has {player.money} chips", end='\n\n')

        index: int = findPlayer(player_dictionary, player)
        player_dictionary[player.type][index]["money"] = player.money

    # reset game
    selected_table.reset_table()
    saveGame()

    # ask for quit
    player_prompt = prompts_responses["prompts"]["new_round"]
    player_response = playerInput(player_prompt, ['yes', 'no'])
    
    if player_response == 'no':
        break
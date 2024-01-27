from helpers import *
from entropy import *

turn = 1
num_turns = 4
deck = createNewDeck()

seat_positions:list = [1,2,3,4]
bot_names:list = ['Randy', 'John', 'Joe', 'Bobby', 'Jeoffry', 'Jinx', 'Jerome']

seat_position = getSeatPosition(seat_positions)

player_directory = Players()

player_name_prompt = 'What is your name?: '
while True:
    player_name = input(player_name_prompt)

    if player_name == '6d1b7d31-238f-46dd-9c7f-7dd281e53feb':
        player_name_prompt = 'Invalid player_name, please enter a different name: '
    else:
        break

createPlayer(player_directory, player_name, 100, seat_position)
player_directory.add_player(Hand(player_name, 100, seat_position), seat_position)

while len(seat_positions) > 0:
    pop_index = randint(0, len(bot_names) - 1)
    cpu_seat_position = getSeatPosition(seat_positions)
    createPlayer(player_directory, bot_names.pop(pop_index), 100, cpu_seat_position)

# create dealer
createPlayer(player_directory, '6d1b7d31-238f-46dd-9c7f-7dd281e53feb', 10000000, 5)

dealCards(deck, 5, player_directory)

first_player = player_directory.get_player_by_name(player_name)

print(player_directory.show_dealer_up_card())
print()
print(first_player.show_hand())

while turn < 6:
    current_player = player_directory.get_player_by_seat(turn)
    hand_value = current_player.count_hand()
    dealer = player_directory.get_player_by_name('Dealer')
    dealer_up_card = player_directory.get_dealer_up_card()

    if current_player.player_name == player_name:
        print(f'Current hand value is {first_player.count_hand()}\n')
        player_hs:str = input('Would you like to hit or stand?: ')
        if player_hs.lower() == 'hit':
            first_player.add_card(deck.deal_card())
        elif player_hs.lower() == 'stand':
            print(f'you stood with a hand of: {first_player.show_hand()} with a value of {first_player.count_hand()}\n')
    
    elif current_player.player_name != '6d1b7d31-238f-46dd-9c7f-7dd281e53feb':
        print(f'{current_player.show_hand()} value: {current_player.count_hand()}')

        shouldHit = False;

        if dealer_up_card >= 7 and hand_value >= 12:
            shouldHit = True;
        elif 1 < dealer_up_card < 4 and hand_value == 12:
            shouldHit = True;
        elif dealer_up_card > 9 and hand_value == 10:
            shouldHit = True;
        elif dealer_up_card == 2 or dealer_up_card >= 7 and hand_value == 9:
            shouldHit = True;
        elif hand_value == 8:
            shouldHit = True;

        if shouldHit:
            current_player.add_card(deck.deal_card())
            print(f'{current_player.player_name} Hit\n')
        else:
            print(f'{current_player.player_name} Stood\n')
    else:
        dealer.show_hand()
        dealer_hand_value = dealer.count_hand()
        if dealer_hand_value < 17:
            dealer.add_card(deck.deal_card())
            if dealer.count_hand() > 21:
                print('The dealer busted!')

            else: 
                print(f'The dealer hit\nValue: {dealer.count_hand()}\n')
        else:
            print(f'The dealer stood with a hand value of {dealer.count_hand()}\n')

    turn += 1
    print(current_player.show_hand() + f'value: {current_player.count_hand()}\n')

    if len(deck.cards) < 5:
        new_deck = createNewDeck()
        deck.append_deck(new_deck.cards)


## New game
from entropy import *
from helpers import *
from enum import Enum


class State(Enum):
    BET = 1
    DEAL = 2
    HS = 3
    PAYOUT = 4

def main():
    player_seat_position = randint(1,4)
    seat_turn = 1
    money = 100
    new_deck = create_deck()
    play_deck = shuffle_deck(new_deck, 12)
    current_state = State.BET

    # Game loop
    while True:

        if current_state == State.BET:
            bet_prompt = 'Please enter a bet: '
            while True:
                bet = int(input(bet_prompt))
                if bet > money:
                    bet_prompt = f"You don't have enough for this bet, please make a bet that is equal to or below {money} dollars: "
                else:
                    current_state = State.DEAL
                    break

        
        if current_state == State.DEAL:
            player_hands = deal_cards(play_deck, 4)
            play_deck = player_hands.deck
            print(f"your hand: {player_hands.player_one_hand}")
            hand_count = count_hand(player_hands.player_one_hand)
            print(f"your current hand value is {hand_count}")
            
            # new line
            print()
            current_state = State.HS


        if current_state == State.HS:
            while seat_turn < 5:
                if seat_turn == player_seat_position:
                    hs_prompt = 'Would you like to hit or stand? [h/s]: '
                    while True:
                        hs_response = input(hs_prompt)

                        if hs_response != 'h' and hs_response != 's':
                            hs_response = 'Please either hit or stand [h/s]: '
                    
                        elif hs_response == 's':
                            print(f"your hand: {player_hands.player_one_hand}")
                            print(f"your current hand value is {hand_count}")
                            break

                        elif hs_response == 'h':
                            player_hands.player_one_hand.append(play_deck.pop(0))
                            print(f"your hand: {player_hands.player_one_hand}")
                            hand_count = count_hand(player_hands.player_one_hand)
                            
                            if hand_count > 21:
                                print(f'you busted! Your hand is worth {hand_count}')
                                break

                            print(f"your current hand value is {hand_count}")


                    seat_turn += 1
                        
                else:
                    seat_turn += 1
            current_state = State.PAYOUT
        
        if current_state == State.PAYOUT:
            print('all done')
            break
            

        # print(entropy_value(deck, shuffled_deck))

if __name__ == '__main__':
    main()



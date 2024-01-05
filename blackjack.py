## New game
from entropy import *
from helpers import *
from enum import Enum


class State(Enum):
    BET = 1
    DEAL = 2
    PLAYERTURN = 3
    CPUTURN = 4
    PAYOUT = 5


def main():
    money = 100
    deck = create_deck()
    shuffled_deck = shuffle_deck(deck, 12)
    current_state = State.BET

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
        deal_cards(deck, 4)
        

    # print(entropy_value(deck, shuffled_deck))

if __name__ == '__main__':
    main()



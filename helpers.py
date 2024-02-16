from random import randint, choice
from classes import *
import uuid

def shuffle_deck(deck:list[Card], num_shuffles:int) -> list[Card]:
    shuffle_count: int = 1
    current_shuffle:list[Card] = deck

    # Prep work for the shuffle, creates two deck halves to be shuffled together using a random cut location
    while shuffle_count <= num_shuffles:
        #clear the two halves to be re-filled with new values from the current_shuffle
        left_half:list[Card] = []
        right_half:list[Card] = []

        # Choose a random cut location to break the deck in two parts
        # recombine but inverse to perform a cut
        left_right = cut_deck(current_shuffle)

        current_shuffle = left_right.right_half + left_right.left_half

        # cut again then reassign halves
        left_right = cut_deck(current_shuffle)

        left_half = left_right.left_half
        right_half = left_right.right_half

        # clear the current shuffle so it can be re-filled with new values
        current_shuffle = []

        length_left = len(left_half)
        length_right = len(right_half)

        # create counters for when a hand is skipped due to RNG
        left_skip_count:int = 0
        right_skip_count:int = 0

        # This loop will perform the bridge shuffle one time
        while True:

            # generate bool for determining which hand will append cards
            left_go:bool = choice([True, False])
            right_go:bool = choice([True, False])

            # if the hand has been skipped twice and would be skipped again, automatically set it to true
            if left_skip_count > 1 and left_go == False:
                left_go = True
            if right_skip_count > 1 and right_go == False:
                right_go = True

            # determine a jitter multiplier to increase randomness on how many cards append per hand per loop
            left_jitter:range = range(0,randint(1,2))
            right_jitter:range = range(0, randint(1,2))

            # if either hand would go negative from the multiplier ensure that the loop will only trigger once
            if length_left - len(left_jitter) < 0:
                left_jitter = range(0,0)
            if length_right - len(right_jitter) < 0:
                right_jitter = range(0,0)

            # This is where cards mix: check if the left and/or right deck should fire, if so append cards 
            # according to the multiplier, if not increment skip count
            if left_go:
                for i in left_jitter: 
                    current_shuffle.append(left_half[length_left-1])
                    length_left -= 1
                    left_skip_count = 0
            else:
                left_skip_count += 1

            if right_go:
                for i in right_jitter:
                    current_shuffle.append(right_half[length_right-1])
                    length_right -= 1
                    right_skip_count = 0
            else:
                right_skip_count += 1
            
            # ensure no deck ran out since the last loop, if only one is 
            # empty append any remaining cards from the other then break the loop
                
            if not length_left > 0 and not length_right > 0:
                break    
            
            elif not length_left > 0:
                for i in reversed(range(0,length_right)):
                    current_shuffle.append(right_half[i])
                break

            elif not length_right > 0:
                for i in reversed(range(0,length_left)):
                    current_shuffle.append(left_half[i])
                break
        
        # increment shuffle count
        shuffle_count += 1 

    return current_shuffle

def createNewDeck() -> Deck:
    # create deck object
    deck:Deck = Deck()

    # generate a fresh deck
    deck.create_deck() #deck type is builtins.list

    # save the fresh deck
    fresh_deck:list[Card] = deck.cards #fresh_deck type is builtins.list

    # shuffle the deck and store it in the deck object
    deck.cards = shuffle_deck(fresh_deck, 7) #deck.cards type is builtins.list

    return deck


def cut_deck(deck:list[Card]) -> DeckHalves:

    deck_cut:int = randint(24,32)
    left_half:list[Card] = deck[:deck_cut]
    right_half:list[Card] = deck[deck_cut:]

    dh = DeckHalves(left_half, right_half)

    return dh

def createPlayer(player_dictionary:dict, player_type, player_name:str, money:int) -> str:
    character_id:str = uuid.uuid4().hex
    new_player = Player(player_type, player_name, money, Hand())
    if player_type != 'player':
        player_dictionary[player_type].append(new_player)
    else:
        player_dictionary[player_type][character_id] = new_player
    return character_id
    
def getSeatPosition(seat_positions:list[int]) -> int:
    return seat_positions.pop(randint(0, len(seat_positions) - 1))

def dealCards(deck:Deck, num_players:int, players:list[Player]) -> None:
    # burn a card
    deck.burn_card()
    
    deal_card:int = 1
    while deal_card < 3:
        for player in players:
            player.hand.add_card(deck.deal_card())
        deal_card += 1

def hasNumbers(player_name:str) -> bool:
    for char in player_name:
        if not char.lower() in 'abcdefghijklmnopqrstuvwxyz':
            return True
    return False
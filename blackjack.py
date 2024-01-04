## New game

from random import randint, choice
import numpy as n


def create_deck():

    card_list = []
    
    for i in range(1,53):
        card_list.append(i)

    # suits_list = ['hearts', 'spades', 'diamonds', 'clubs']
    # face_cards = ['Ace', 'Jack', 'Queen', 'King']
    # card_list = []

    # for j in suits_list:
    #     card_list.append(f'{face_cards[0]} of {j}')
    #     for i in range(2,11):
    #         card_list.append(f'{i} of {j}')
    #     for k in range(1,4):
    #         card_list.append(f'{face_cards[k]} of {j}')

    return card_list


def shuffle_deck(deck, num_shuffles):
    shuffle_count = 1
    current_shuffle = deck

    # Prep work for the shuffle, creates two deck halves to be shuffled together using a random cut location
    while shuffle_count <= num_shuffles:
        #clear the two halves to be re-filled with new values from the current_shuffle
        left_half = []
        right_half = []

        # Choose a random cut location to break the deck in two parts
        # slice the current deck state to create left and right halves
        deck_cut = randint(24,32)
        left_half = current_shuffle[:deck_cut]
        right_half = current_shuffle[deck_cut:]

        # recombine halves to complete a cut
        current_shuffle = right_half + left_half

        # cut again then reassign halves
        deck_cut = randint(24,32)
        left_half = current_shuffle[:deck_cut]
        right_half = current_shuffle[deck_cut:]

        # clear the current shuffle so it can be re-filled with new values
        current_shuffle = []

        length_left = len(left_half)
        length_right = len(right_half)

        # create counters for when a hand is skipped due to RNG
        left_skip_count = 0
        right_skip_count = 0

        # This loop will perform the bridge shuffle one time
        while True:

            # generate bool for determining which hand will append cards
            left_go = choice([True, False])
            right_go = choice([True, False])

            # if the hand has been skipped twice and would be skipped again, automatically set it to true
            if left_skip_count > 1 and left_go == False:
                left_go = True
            if right_skip_count > 1 and right_go == False:
                right_go = True

            # determine a jitter multiplier to increase randomness on how many cards append per hand per loop
            left_jitter = range(0,randint(1,2))
            right_jitter = range(0, randint(1,2))

            # if either hand would go negative from the multiplier ensure that the loop will only trigger once
            if length_left - len(left_jitter) < 0:
                left_jitter = [0]
            if length_right - len(right_jitter) < 0:
                right_jitter = [0]

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
            
            
            
def main():

    distance_array = []
    j = 0

    for shuffle in range(0,1):
        fresh_deck = create_deck()
        shuffled_deck = shuffle_deck(fresh_deck, 100)
        for i in range(0,51):
            if i == 50:
                distance_adjacent = fresh_deck.index(shuffled_deck[0]) - fresh_deck.index(shuffled_deck[i + 1])
                if distance_adjacent < 0:
                    distance_adjacent += 52
                distance_array.append(distance_adjacent)
    
            distance_adjacent = fresh_deck.index(shuffled_deck[i + 1]) - fresh_deck.index(shuffled_deck[i])

            if distance_adjacent < 0:
                distance_adjacent += 52

            distance_array.append(distance_adjacent)
    
    histogram_array = []
    for i in range(0,52):
        histogram_array.append(i)

    for l in histogram_array:
        count = 0
        for k in distance_array:
            if k == l:
                count += 1
        histogram_array[l] = count/52

    entropy_array = []
    for i in histogram_array:
        if i == 0:
            entropy_array.append(0)
            continue
        e = -i * n.log(i)
        entropy_array.append(e)
        
    print(sum(entropy_array))



if __name__ == '__main__':
    main()



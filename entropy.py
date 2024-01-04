import numpy as n

# determine randomness of shuffle
    
def entropy_value(fresh_deck, shuffled_deck):
    distance_array = []
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
        
    e = sum(entropy_array)

    return e


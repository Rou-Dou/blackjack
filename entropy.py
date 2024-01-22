import numpy as n
from classes import Card

# determine randomness of shuffle
def entropy_value(fresh_deck:list[Card], shuffled_deck:list[Card]) -> float:
    distance_array:list[int] = []
    for i in range(0,51):
        if i == 50:
            distance_adjacent:int = fresh_deck.index(shuffled_deck[0]) - fresh_deck.index(shuffled_deck[i + 1])
            if distance_adjacent < 0:
                distance_adjacent += 52
            distance_array.append(distance_adjacent)

        distance_adjacent = fresh_deck.index(shuffled_deck[i + 1]) - fresh_deck.index(shuffled_deck[i])

        if distance_adjacent < 0:
            distance_adjacent += 52

        distance_array.append(distance_adjacent)

    histogram_array:list[float] = []

    for index in range(0,52,1):
        count:int = 0
        for distance in distance_array:
            if distance == index:
                count += 1
        histogram_array.append(float(count/52))

    entropy_array:list[float] = []

    for item in histogram_array:
        if item == 0.0:
            entropy_array.append(0.0)
            continue
        e:float = -item * n.log(item)
        entropy_array.append(e)
        
    e = sum(entropy_array)

    return e
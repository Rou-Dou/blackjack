from classes import *
from random import randint, choice
import uuid
import json
from typing import Any


def initGame() -> dict[str, Any]:

    txt_file = open('player_dictionary.json', 'r')
    player_dictionary: dict[str, Any] = json.load(txt_file)
    txt_file.close()

    # generate cpu and dealer on first launch
    if len(player_dictionary['cpu']) == 0 or len(player_dictionary['dealer']) == 0:
        bot_txt = open('bot_names.txt', 'r')
        bot_names: list[str] = []

        for line in bot_txt:
            bot_names.append(line.strip())

        while len(bot_names) > 0:
            createPlayer(player_dictionary, 'cpu', bot_names.pop(0), 2000, 0)

        createPlayer(player_dictionary, 'dealer', 'Dealer', 10000000, 0)

        bot_txt.close()

    return player_dictionary


def findPlayer(player_dictionary: dict[str, Any], player: Player) -> int:
    try:
        for index, player_object in enumerate(player_dictionary[player.type]):
            if player.player_name == player_object['player_name']:
                break
    except ValueError:
        index = -1
    return index


def saveGame(player_dictionary: dict[str, Any]) -> None:
    txt_file = open('player_dictionary.json', 'w')
    json.dump(player_dictionary, txt_file)
    txt_file.close()


def player_bet_input(player: Player) -> int:

    print(f'You have {player.money} chips.')
    sleep(1)

    bet_string: str = 'please enter a bet: '
    
    while True:
        player_bet: str = input(bet_string)
        for char in player_bet:
            if char not in '1234567890':
                bet_string = 'Your bet must be a whole number: '
                break
        
        if int(player_bet) > player.money:
            bet_string = f'You cannot bet more money than you have. You currently have {player.money} dollars: ' 
            continue

        return int(player_bet)
    

def createPlayerCharacter(player_dictionary: dict[str, Any]) -> None:
    # create player character
    player_name_prompt: str = 'What is your players name?: '

    # Character creation loop
    while True:
        player_name = input(player_name_prompt).strip()

        if player_name.lower().find('dealer') != -1:
            player_name_prompt = 'Invalid player_name, please enter a different name: \n'
        elif hasNumbers(player_name):
            player_name_prompt = 'Please only include alphabetical characters in your name: \n'
        else:
            break
    createPlayer(player_dictionary, "player", player_name, 2000, 0)

    txt_file = open('player_dictionary.json', 'w')
    json.dump(player_dictionary, txt_file)
    txt_file.close()
        

def populate_table(table: Table, player_dictionary: dict[str, Any]) -> Table:
    empty_player: Player = Player('', '', '', 0, 0)
    players: list[Player] = []
    dealer = player_dictionary['dealer'][0]
    rand_num: int = randint(1,100)
    while len(players) < 10:
        repeat:bool = False
        selected_player: dict[str, Any] = (player_dictionary['cpu'][randint(0, len(player_dictionary['cpu']) - 1)])
        for player in players:
            if player.player_name == selected_player['player_name']:
                repeat = True

        if not repeat:
            players.append(Player(selected_player['player_id'], 'cpu', selected_player["player_name"], selected_player["money"], selected_player["affinity"]))
    
    while len(table.table_seats) < 4:
        rand_num = randint(1,100)
        if rand_num > 50:
            table.table_seats.append(empty_player)
        else:
            table.table_seats.append(players.pop(randint(0, len(players) - 1)))
    table.table_seats.append(Player(dealer['player_id'], 'dealer', dealer['player_name'], dealer['money'], dealer['affinity']))
    
    return table


def shuffle_deck(deck: list[Card], num_shuffles: int) -> list[Card]:
    shuffle_count: int = 1
    current_shuffle: list[Card] = deck

    # Prep work for the shuffle, creates two deck halves to be shuffled together using a random cut location
    while shuffle_count <= num_shuffles:
        #clear the two halves to be re-filled with new values from the current_shuffle
        left_half: list[Card] = []
        right_half: list[Card] = []

        # Choose a random cut location to break the deck in two parts
        # recombine but inverse to perform a cut
        left_right: dict[str, list[Card]] = cut_deck(current_shuffle)

        current_shuffle: list[Card] = left_right["right_half"] + left_right["left_half"]

        # cut again then reassign halves
        left_right = cut_deck(current_shuffle)

        left_half = left_right["left_half"]
        right_half = left_right["right_half"]

        # clear the current shuffle so it can be re-filled with new values
        current_shuffle = []

        length_left: int = len(left_half)
        length_right: int = len(right_half)

        # create counters for when a hand is skipped due to RNG
        left_skip_count: int = 0
        right_skip_count: int = 0

        # This loop will perform the bridge shuffle one time
        while True:

            # generate bool for determining which hand will append cards
            left_go: bool = choice([True, False])
            right_go: bool = choice([True, False])

            # if the hand has been skipped twice and would be skipped again, automatically set it to true
            if left_skip_count > 1 and left_go == False:
                left_go = True
            if right_skip_count > 1 and right_go == False:
                right_go = True

            # determine a jitter multiplier to increase randomness on how many cards append per hand per loop
            left_jitter: range = range(0,randint(1,2))
            right_jitter: range = range(0, randint(1,2))

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
    deck: Deck = Deck()

    # generate a fresh deck
    deck.create_deck()

    # save the fresh deck
    fresh_deck: list[Card] = deck.cards

    # shuffle the deck and store it in the deck object
    deck.cards = shuffle_deck(fresh_deck, 7)

    return deck


def cut_deck(deck: list[Card]) -> dict[str, list[Card]]:
    '''
    Takes a provided 52 card deck and breaks it into two halves at a random point near the center.
    Returns an object with two attribues "left_half" and "right_half"

    >> cut_deck([1,2,3,4,5]) \n
    {
        "left_half" : [1,2],
        "right_half" : [3,4,5]
    }

    >> cut_deck([1,5,6,10,15,3,2,5]) \n
    {
        "left_half" : [1,5,6,10,15]
        "right_half" : [3,2,5]
    }
    '''

    deck_cut: int = randint(24,32)
    left_half: list[Card] = deck[:deck_cut]
    right_half: list[Card] = deck[deck_cut:]

    dh = {"left_half" : left_half,
          "right_half" : right_half}

    return dh


def createPlayer(player_dictionary: dict[str, Any], player_type: str, player_name: str, money: int, affinity: int) -> Player:
    character_id: str = uuid.uuid4().hex
    new_player = Player(character_id, player_type, player_name, money, affinity)
    player_dictionary[player_type].append(new_player.__toJSON())
    return new_player
    

def getSeatPosition(seat_positions: list[int]) -> int:
    return seat_positions.pop(randint(0, len(seat_positions) - 1))


def dealCards(dealer: Dealer, players: list[Player]) -> None:
    # burn a card
    dealer.burn_card()
    
    deal_card: int = 1
    while deal_card < 3:
        for player in players:
            if player.type == '':
                continue
            dealer.deal_card(player.hands[0])
        deal_card += 1


def hasNumbers(player_name: str) -> bool:
    for char in player_name:
        if not char.lower() in 'abcdefghijklmnopqrstuvwxyz':
            return True
    return False


def resetTable(table: Table, dictionary: dict[str, Any]) -> None:
    i = 0
    leaving_players = []
    for player in table.table_seats:
        player.hands = []
        player.bet = 0
        rand = randint(1,100)
        if (player.money < 500 or player.over == True) and (player.type != 'dealer' and player.type != 'player'):
            player.over = False
            if rand > 80:
                leaving_players.append(i)
                continue
        i += 1
    
    #remove players who left the table
    for index in leaving_players:
        table.table_seats.pop(index)

    populate_table(table, dictionary)


def checkPlayerBust(player: Player) -> bool:
    overMessage: str = ''
    if player.type == 'player':
        overMessage = 'You busted!'
    else:
        overMessage = f'{player.player_name} busted!'

    for hand in player.hands:
        if hand.count_hand() > 21:
            if player.type != 'dealer':
                player.money -= player.bet
            print(overMessage)
            player.__setStatus(True)
            return True
    return False
    

def typeWriter(string) -> None:
    build_string: str = ''
    for count, char in enumerate(string):
        if count == len(string) - 1:
            build_string += char
            print(build_string, end="")
            print()
            sleep(0.05)
        else:
            build_string += char
            print(build_string, end="")
            print("\r", end="")
            sleep(0.05)
    sleep(0.5)
        
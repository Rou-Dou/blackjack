from classes import *
from misc_functions import *
import uuid
import json
with open('prompts_responses.json', 'r') as json_file:
    prompts_responses: dict[str, Any] = json.load(json_file)


def initGame() -> dict[str, Any]:
    '''
    Instantiates the player_dictionary. This includes populating
    the player dictionary if the game has never been launched.
    '''

    # generate cpu and dealer on first launch
    if len(player_dictionary['cpu']) == 0 or len(player_dictionary['dealer']) == 0:
        bot_txt = open('bot_names.txt', 'r')
        bot_names: list[str] = []

        for line in bot_txt:
            bot_names.append(line.strip())

        while len(bot_names) > 0:
            createPlayer('cpu', bot_names.pop(0), 2000, 0)

        bot_txt.close()

    return player_dictionary


def findPlayer(player_dictionary: dict[str, Any], player: Player) -> int:
    '''
    Retrieve a players index location in the dictionary player list.
    If the player cannot be found return -1.

    >>> findPlayer(player_dictionary, Player('id123', 'john', 'cpu', 0, 0)
    12

    >>> findPlayer(player_dictionary, Player('id124', 'mary', 'player', 0, 0))
    -1
    '''
    try:
        for index, player_object in enumerate(player_dictionary[player.type]):
            if player.id == player_object['player_id']:
                break
    except ValueError:
        index = -1
    return index


def saveGame() -> None:
    '''
    Writes all game information to json file.
    '''
    with open('player_dictionary.json', 'w') as txt_file:
        json.dump(player_dictionary, txt_file)


def playerBetInput(player: Player) -> int:
    '''
    Handles player bet input, ensuring that the player
    has entered an integer value and a value that they
    can afford.
    '''
    print(f'You have {player.money} chips')
    sleep(1)

    bet_string: str = prompts_responses["prompts"]["bet"]
    
    while True:
        player_bet: str = input(bet_string)

        if not player_bet.isdigit():
            bet_string = prompts_responses["errors"]["invalid_bet_input"]
            continue
        
        if int(player_bet) > player.money:
            bet_string = 'f{prompts_responses["errors"]["insufficient_money"]}\
            you currently have {player.money} chips.\nPlease make another bet: '
            continue

        return int(player_bet)
    

def playerInput(prompt: str, valid_inputs: list[str]) -> str:
    '''
    Generic function intended to handle string input
    prompts_responses. You provide a prompt and valid inputs. This
    will ensure the string is valid and that the user enters
    one of the valid inputs. Returns the users input.

    Conditions:\n
    valid inputs should always be lower case with no spaces

    >>> player_input('enter yes or no', [yes, no])
    'yes'
    '''
    player_input: str = ''

    while True:   
        player_input = input(prompt)

        if player_input.replace(' ', '').isalpha():
            player_input = player_input.lower().replace(" ", "")
        else:
            continue
        
        if player_input in valid_inputs:
            break

    return player_input
        
    

def createPlayerCharacter() -> None:
    '''
    Takes a player name from a user input and creates a player class using
    the `createPlayer()` function.
    '''
    # create player character
    player_name_prompt: str = 'What is your players name?: '

    # Character creation loop
    while True:
        player_name = input(player_name_prompt).strip()

        if player_name.lower().find('dealer') != -1:
            player_name_prompt = 'Invalid player name, please enter a different name: \n'
        elif not player_name.isalpha() :
            player_name_prompt = 'Please only include alphabetical characters in your name: \n'
        else:
            break

    createPlayer("player", player_name, 2000, 0)
    
    saveGame()


def createPlayer(player_type: str, player_name: str, money: int, affinity: int) -> Player:
    '''
    Takes player class constructor inputs and creates a new player, adding the information
    to the player dictionary and returning the player object. This function is used primarily for
    populating the tables.
    '''
    character_id: str = uuid.uuid4().hex
    new_player: Player = Player(character_id, player_type, player_name, money, affinity)

    player_dictionary[player_type].append(new_player.to_json())

    return new_player


# logic here is based on 'ideal' blackjack play at a basic level
# A simple series of dealer/player conditions are considered for when the CPU
# should hit, otherwise `shouldHit` is false by default and the CPU will stand.
def shouldHit(dealer_up_card_value, hand_value) -> bool:
    shouldHit: bool = False
    if dealer_up_card_value >= 7 and 12 <= hand_value <= 16:
        shouldHit = True
    elif 1 < dealer_up_card_value < 4 and hand_value == 12:
        shouldHit = True
    elif dealer_up_card_value > 9 and hand_value == 10:
        shouldHit = True
    elif dealer_up_card_value == 2 or dealer_up_card_value >= 7 and hand_value == 9:
        shouldHit = True
    elif hand_value == 8:
        shouldHit = True

    return shouldHit

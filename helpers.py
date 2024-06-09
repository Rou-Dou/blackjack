from classes import *
from misc_functions import *
import uuid
import json


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

    print(f'You have {player.money} chips')
    sleep(1)

    bet_string: str = 'please enter a bet: '
    
    while True:
        player_bet: str = input(bet_string)
        for char in player_bet:
            if not char.isdigit():
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
            player_name_prompt = 'Invalid player name, please enter a different name: \n'
        elif not player_name.isalpha() :
            player_name_prompt = 'Please only include alphabetical characters in your name: \n'
        else:
            break

    createPlayer(player_dictionary, "player", player_name, 2000, 0)
    
    saveGame(player_dictionary)
        

def populate_table(table: Table, player_dictionary: dict[str, Any]) -> Table:
    players: list[Player] = []
    rand_num: int = -1

    while len(players) < 10:
        repeat: bool = False
        selected_player: dict[str, Any] = (player_dictionary['cpu'][randint(0, len(player_dictionary['cpu']) - 1)])
        for player in players:
            if player.player_name == selected_player['player_name']:
                repeat = True

        if not repeat:
            players.append(Player(selected_player['player_id'], 'cpu', selected_player["player_name"], selected_player["money"], selected_player["affinity"]))
    
    while len(table.table_seats) < 4:
        rand_num = randint(1,100)
        if rand_num > 50:
            table.table_seats.append(None)
        else:
            table.table_seats.append(players.pop(randint(0, len(players) - 1)))    
    return table


def createPlayer(player_dictionary: dict[str, Any], player_type: str, player_name: str, money: int, affinity: int) -> Player:
    character_id: str = uuid.uuid4().hex
    new_player = Player(character_id, player_type, player_name, money, affinity)
    player_dictionary[player_type].append(new_player.toJSON())
    return new_player
    

def dealCards(dealer: Dealer, players: list[Union[Player, None]]) -> None:

    dealer.burn_card()
    
    deal_card: int = 1
    while deal_card < 3:
        for player in players:
            if player is None:
                continue
            dealer.deal_card(player.hands[0])
        dealer.deal_self()
        deal_card += 1


def resetTable(table: Table, dictionary: dict[str, Any]) -> None:

    leaving_players: list[int] = []
    for i, player in enumerate(table.table_seats):
        if player is not None:
            player.hands = []
            player.bet = 0
            rand = randint(1,100)

            if (player.money < 500 or player.over) and (player.type != 'player') and rand > 80:
                leaving_players.append(i)

            player.over = False
    
    #remove players who left the table
    for index in leaving_players:
        table.table_seats.pop(index)

    populate_table(table, dictionary)
        

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
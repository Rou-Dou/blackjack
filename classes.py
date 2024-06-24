from enum import Enum
import json
from time import sleep
from typing import Any, Union, Iterator
from random import randint, choice
import uuid

with open('player_dictionary.json','r') as json_file:
    player_dictionary: dict[str, Any] = json.load(json_file)

with open('card_values.json', 'r') as vd:
    card_values: dict[str, int] = json.load(vd)


class Faces(Enum):
    Ace = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine =  9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13

class Suits(Enum):
    Clubs = 1
    Hearts = 2
    Spades = 3
    Diamonds = 4


class Card:
    '''
    Card class, carries thte face, suit, and value properties for each card in the game
    available methods include\n `show_card()`
    '''
    def __init__(self, face: str, suit: str, value: int) -> None:
        self.face: str = face
        self.suit: str = suit
        self.value: int = value


    def show_card(self) -> str:
        return f'{self.face} of {self.suit}'


class Hand:
    '''
    This class handles hands for players. Each hand contains a list of `Card()` classes\n
    Methods include:\n
    `add_card()`\n
    `count_hand()`\n
    `has_ace()`\n
    `print_hand()`\n
    `clear_hand()`
    '''
    def __init__(self) -> None:
        self.cards: list[Card] = [] #hand is type list with object
        self.value: int = 0

    def __str__(self) -> str:
        hand_str: str = ''
        
        hand_str += "Hand Contents: \n\n"

        for position, card in enumerate(self.cards, 1):
            hand_str += (f'{position}: {card.show_card()}\n')
        
        hand_str += f'\nValue: {self.value}'

        return hand_str

    def __iter__(self) -> Iterator:
        return iter(self.__str__())
    
    def __next__(self) -> None:
        pass


    def add_card(self, card: Card) -> None:
        self.cards.append(card)
        self._add_value(card)

    
    def _add_value(self, card: Card) -> None:
        new_value = self.value + card.value

        if new_value > 21 and card.face == 'Ace':
            card.value = 1
        
        self.value += card.value

    def clear_hand(self) -> None:
        self.cards.clear()


class Deck:
    '''
    The deck class handles all interactions involving the deck of cards.
    The primary contents are a list of `Card()` classes. Two internal functions
    construct the decks contents and shuffle them.\n
    Methods include:\n
    `append_deck()`\n
    `is_thin()`\n
    `num_cards()`
    '''
    def __init__(self) -> None:
        self.cards: list[Card] = [] #cards is a list of class Card
        self._create_deck()
        self._shuffle_deck(7)


    def _create_deck(self) -> None:
        for suit in Suits:
            for face in Faces:
                self.cards.append(Card(face.name, suit.name, card_values[face.name]))


    def append_deck(self, deck: "Deck") -> None:
        self.cards = self.cards + deck.cards

    def is_thin(self) -> bool:
        if len(self.cards) < 15:
            return True
        return False


    def num_cards(self) -> int:
        return len(self.cards)
    

    def _cut_deck(self) -> dict[str, list[Card]]:
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
        deck_half: int = len(self.cards)//2
        deck_cut: int = randint(deck_half - 5, deck_half + 5)
        left_half: list[Card] = self.cards[:deck_cut]
        right_half: list[Card] = self.cards[deck_cut:]

        dh = {
                "left_half" : left_half,
                "right_half" : right_half
            }

        return dh
    

    def _shuffle_deck(self, num_shuffles: int) -> None:
        shuffle_count: int = 1
        current_shuffle: list[Card] = []
        left_half: list[Card] = []
        right_half: list[Card] = []

        # Prep work for the shuffle, creates two deck halves to be shuffled together using a random cut location
        while shuffle_count <= num_shuffles:

            # Choose a random cut location to break the deck in two parts
            # recombine but inverse to perform a cut
            left_right: dict[str, list[Card]] = self._cut_deck()
            self.cards = left_right["right_half"] + left_right["left_half"]

            # cut again then reassign halves
            left_right = self._cut_deck()

            length_left: int = len(left_right["left_half"])
            length_right: int = len(left_right["right_half"])

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
                        current_shuffle.append(left_right["left_half"].pop())
                        length_left -= 1
                        left_skip_count = 0
                else:
                    left_skip_count += 1

                if right_go:
                    for i in right_jitter:
                        current_shuffle.append(left_right["right_half"].pop())
                        length_right -= 1
                        right_skip_count = 0
                else:
                    right_skip_count += 1
                
                # ensure no deck ran out since the last loop, if only one is 
                # empty append any remaining cards from the other then break the loop
                    
                if length_left == 0 and length_right == 0:
                    break   
                
                elif length_left == 0:
                    for i in reversed(range(0,length_right)):
                        current_shuffle.append(left_right["right_half"][i])
                    break

                elif length_right == 0:
                    for i in reversed(range(0,length_left)):
                        current_shuffle.append(left_right["left_half"][i])
                    break
            
            # increment shuffle count
            self.cards = current_shuffle
            shuffle_count += 1 
            current_shuffle = []


class Player:
    '''
    The player class contains all information for both human and cpu players.
    the constructor requires an id, a type, a player_name, money, and an affinity value.\n
    Methods include:\n
    `print_player_hand()`\n
    `toJSON()`\n
    `isPlayer()`\n
    `makeBet()`\n
    `setStatus()`\n
    `createHand()`\n
    `affinityUp()`\n
    `affinityDown()`\n
    `hasTwentyOne()`\n
    `isOver()`\n


    '''
    def __init__(self, id: str, type: str, player_name: str, money: int, affinity: int) -> None:
        self.id: str = id
        self.type: str = type
        self.player_name: str = player_name
        self.money: int = money
        self.hands: list[Hand] = []
        self.over: bool = False
        self.affinity: int = affinity
    

    def to_json(self) -> dict[str,Any]:
        playerDict: dict[str, Any] = {}
        playerDict["player_id"] = self.id
        playerDict["player_name"] = self.player_name
        playerDict["money"] = self.money
        playerDict["affinity"] = self.affinity
        return playerDict
    
    def is_player(self) -> bool:
        if self.type == 'player':
            return True
        return False
    

    def make_bet(self, bet: int, min_bet: int) -> None:
        if bet < min_bet:
            bet = min_bet
        
        if bet > self.money:
            bet = self.money
            print(f'{self.player_name} went all in')
            sleep(2)
            

        elif self.type == 'cpu':
            bet = self._get_bet(min_bet)

        self.bet = bet


    def _generated_uuid(self) -> None:
        if self.id == '':
            self.id = uuid.uuid4().hex

        
    def _get_bet(self, min_bet: int) -> int:
        dice_roll: int = randint(1,6)
        reroll: int = randint(1,6)
        matches: int = 0
        low: int = -1
        high :int = -1

        while reroll == dice_roll:
            reroll = randint(1,6)
            matches += 1
        match matches:
            case 0:
                low, high = min_bet, min_bet*2
            case 1:
                low, high = min_bet*2, min_bet*3
            case 2: 
                low, high = min_bet*3, min_bet*4
            case _:
                low, high = min_bet*4, self.money
        
        bet: int = randint(low, high)

        mod_value: int = bet % 5

        if mod_value < 3:
            bet = bet - mod_value 
        else:
            bet = bet + (5 - mod_value)

        return bet


    def set_status(self, over: bool) -> None:
        self.over = over


    def create_hand(self) -> None:
        new_hand: Hand = Hand()
        self.hands.append(new_hand)


    def affinity_up(self) -> None:
        self.affinity += 1
    

    def affinity_down(self) -> None:
        self.affinity -= 1


    def has_twenty_one(self, hand: Hand) -> bool:
        end_string: str = ""
        player_type_str: str = ""
        hand_length: int = len(hand.cards)
        has_twenty_one: bool = hand.value == 21

        # If player has 21 stand automatically
        if has_twenty_one:
            self.set_status(False)

            match hand_length:
                case 2:
                    end_string = "got blackjack!"
                case _:
                    end_string = "got 21!"

            if not isinstance(self, Dealer):
                match self.type:
                    case "player":
                        player_type_str = 'You'
                    case "cpu":
                        player_type_str = self.player_name
            else:
                player_type_str = 'The dealer'
                
            print(f'{player_type_str} {end_string}')
            return True
        
        return False
    

    def has_busted(self) -> bool:
        overMessage: str = ''

        for hand in self.hands:
            if hand.value > 21:
                self.set_status(True)

                if isinstance(self, Player) and not isinstance(self, Dealer):
                    match self.type:
                        case "player":
                            overMessage = 'You busted!'
                        case _:
                            overMessage = f'{self.player_name} busted!'
                    self.money -= self.bet
                else:
                    overMessage = 'The dealer busted!'

                print(overMessage+'\n')
                return True
            
        return False

class Dealer(Player):
    '''
    The dealer class is a subclass of the `Player()` class. it handles all actions of the 
    dealer while inheriting functionality from the player class.\n
    Methods include:\n
    `deal_card()`\n
    `burn_card()`\n
    `get_dealer_up_card()`
    '''
    def __init__(self, id: str, deck: Deck, hand: Hand) -> None:
        self.id: str = id
        self.deck: Deck = deck
        self.over: bool = False
        self.hands: list[Hand] = [hand]


    def deal_card(self, hand:Hand) -> Card:
        dealt_card: Card = self.deck.cards.pop(0)
        hand.add_card(dealt_card)
        return dealt_card
    

    def burn_card(self) -> None:
        self.deck.cards.pop(0)
    

    def _deal_self(self) -> None:
        self.hands[0].add_card(self.deck.cards.pop(0))


    def get_dealer_up_card(self) -> Card:
        return self.hands[0].cards[1]
    

class Table:
    '''
    the table class holds all assigned `Player()` classes in a list 
    as well as a `Dealer()` class. Each table has an assigned
    minimum bet
    Methods include:\n
    `get_open_seats()`\n
    `has_open_seats()`\n
    `print_table_players()`\n
    `reset_table()`\n
    `deal_cards()`
    '''
    def __init__(self, dealer: Dealer, min_bet: int) -> None:
        self.table_seats: list[Union[Player, None]] = []
        self.minimum_bet: int = min_bet
        self.dealer: Dealer = dealer

    def __str__(self) -> str:
        print_str: str = ''
        print_str += f'There are {self._get_num_open_seats()} seat(s) available: \n\n'
        print_str += 'People at this table: \n\n'
        for player in self.table_seats:
            if player is not None:
                print_str += f'{player.player_name}\n'
        print_str += '\n'
        return print_str


    def get_open_seats(self) -> list[int]:
        open_seat_indexes: list[int] = []
        for i, player in enumerate(self.table_seats):
            if player is None:
                open_seat_indexes.append(i)
        return open_seat_indexes
    

    def has_open_seats(self) -> bool:
        if self._get_num_open_seats() < 1:
            return False
        return True
    
    def _get_num_open_seats(self) -> int:
        open_seat_count: int = 0
        for player in self.table_seats:
            if player is None:
                open_seat_count += 1
        return open_seat_count
    

    def reset_table(self) -> None:
        leaving_players: list[int] = []
        for i, player in enumerate(self.table_seats):
            rand: int = randint(1,100)

            if player is None:
                continue

            elif (player.money < 500 or player.over) and (not player.is_player()) and rand > 80:
                leaving_players.append(i)
                continue
            
            else:
                player.hands = []
                player.bet = 0
                rand = randint(1,100)
                player.set_status(False)
        
        #remove players who left the table
        for index in leaving_players:
            self.table_seats.pop(index)
        
        # reset dealer
        self.dealer.hands[0].clear_hand()
        self.dealer.set_status(False)

        self.populate_table()


    def populate_table(self) -> None:
        players: list[Player] = []
        rand_num: int = -1

        while len(players) < 10:
            repeat: bool = False
            selected_player: dict[str, Any] = (
                player_dictionary['cpu'][randint(0, len(player_dictionary['cpu']) - 1)])
            for player in players:
                if player.player_name == selected_player['player_name']:
                    repeat = True

            if not repeat:
                players.append(
                    Player(
                        selected_player['player_id'], 
                        'cpu', 
                        selected_player["player_name"], 
                        selected_player["money"], 
                        selected_player["affinity"]
                    )
                )
        
        while len(self.table_seats) < 4:
            rand_num = randint(1,100)
            if rand_num > 50:
                self.table_seats.append(None)
            else:
                self.table_seats.append(players.pop(randint(0, len(players) - 1)))

    
    def initiate_hand(self) -> None:
        # give each player at the table a hand and deal cards
        for player in self.table_seats:
            if player is not None:
                player.create_hand()

        self.dealer.burn_card()
        
        deal_card: int = 1
        while deal_card < 3:
            for player in self.table_seats:
                if player is None:
                    continue
                self.dealer.deal_card(player.hands[0])
            self.dealer._deal_self()
            deal_card += 1



class Casino:
    def __init__(self, num_tables: int) -> None:
        self.num_tables: int = num_tables
        self.tables: list[Table] = []

    def __str__(self) -> str:
        print_str: str = ''
        for count, table in enumerate(self.tables, 1):
            if not table.has_open_seats():
                print_str += f'Table {count} is full\n\n'
                continue
            print_str += f'Table {count}: \n'
            print_str += f'\033[01m\nminimum bet for this table is {table.minimum_bet}\033[00m\n'

            print_str += table.__str__()

        return print_str
    
    def __iter__(self) -> Iterator:
        return iter(self.__str__())
        
        
    def __next__(self) -> None:
        pass

    def get_table(self, table_number: int) -> Table:
        return self.tables[table_number - 1]
    

    def get_tables(self) -> list[Table]:
        return self.tables
    

    def add_table(self, table: Table) -> None:
        self.tables.append(table)
from enum import Enum
import json
from time import sleep
from typing import Any, Union
from random import randint, choice

json_file = open('value_dictionary.json', 'r')
value_dictionary: dict[str, int] = json.load(json_file)
json_file.close()

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
    def __init__(self, face: str, suit: str, value: int) -> None:
        self.face: str = face
        self.suit: str = suit
        self.value: int = value

    def show_card(self) -> str:
        return f'{self.face} of {self.suit}'


class Hand:
    def __init__(self) -> None:
        self.cards: list[Card] = [] #hand is type list with object

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def count_hand(self) -> int:
        hand_value: int = 0
        for card in self.cards:
            hand_value += card.value
    
        if hand_value > 21 and self.has_ace():
            hand_value -= 10
            
        return hand_value
        
    def has_ace(self) -> bool:
        for card in self.cards:
            if card.face == 'Ace':
                return True
        return False
    
    def print_hand(self) -> None:
        hand_str: str = ''
        
        print("Hand Contents: ")

        for position, card in enumerate(self.cards, 1):
            hand_str += (f'{position}: {card.show_card()}\n')
        print(hand_str)
    
    def clear_hand(self) -> None:
        self.cards.clear()


class Deck:
    def __init__(self) -> None:
        self.cards: list[Card] = [] #cards is a list of class Card
        self.__create_deck()
        self.__shuffle_deck(7)

    def __create_deck(self) -> None:
        for suit in Suits:
            for face in Faces:
                self.cards.append(Card(face.name, suit.name, value_dictionary[face.name]))
    
    def get_deck(self) -> None:
        for card in self.cards:
            card.show_card()

    def append_deck(self, deck: "Deck") -> None:
        self.cards = self.cards + deck.cards

    def num_cards(self) -> int:
        return len(self.cards)
    
    def __cut_deck(self) -> dict[str, list[Card]]:
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
    

    def __shuffle_deck(self, num_shuffles) -> None:
        shuffle_count: int = 1
        current_shuffle: list[Card] = []
        left_half: list[Card] = []
        right_half: list[Card] = []

        # Prep work for the shuffle, creates two deck halves to be shuffled together using a random cut location
        while shuffle_count <= num_shuffles:

            # Choose a random cut location to break the deck in two parts
            # recombine but inverse to perform a cut
            left_right: dict[str, list[Card]] = self.__cut_deck()
            self.cards = left_right["right_half"] + left_right["left_half"]

            # cut again then reassign halves
            left_right = self.__cut_deck()
            left_half = left_right["left_half"]
            right_half = left_right["right_half"]

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
                        current_shuffle.append(left_half.pop())
                        length_left -= 1
                        left_skip_count = 0
                else:
                    left_skip_count += 1

                if right_go:
                    for i in right_jitter:
                        current_shuffle.append(right_half.pop())
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
                        current_shuffle.append(right_half[i])
                    break

                elif length_right == 0:
                    for i in reversed(range(0,length_left)):
                        current_shuffle.append(left_half[i])
                    break
            
            # increment shuffle count
            self.cards = current_shuffle
            shuffle_count += 1 
            current_shuffle = []





class Player:
    def __init__(self, id:str, type: str, player_name: str, money: int, affinity: int) -> None:
        self.id: str = id
        self.type: str = type
        self.player_name: str = player_name
        self.money: int = money
        self.hands: list[Hand] = []
        self.affinity: int = affinity
    
    def print_player_hand(self) -> None:
        for count, hand in enumerate(self.hands, 1):
            f"Hand {count}:\n"
            f"\t{hand.print_hand()}"
            print(f'with a value of {hand.count_hand()}\n')
    
    def toJSON(self) -> dict[str,Any]:
        playerDict: dict[str, Any] = {}
        playerDict["player_id"] = self.id
        playerDict["player_name"] = self.player_name
        playerDict["money"] = self.money
        playerDict["affinity"] = self.affinity
        return playerDict
    
    def makeBet(self, bet: int) -> None:
        if bet > self.money:
            bet = self.money
            print(f'{self.player_name} went all in')
            sleep(2)

        elif self.type == 'cpu':
            bet = self.__getBet()

        self.bet = bet

        
    def __getBet(self) -> int:
        dice_roll: int = randint(1,6)
        reroll: int = randint(1,6)
        matches: int = 0
        low: int = 0
        high :int = 0

        while reroll == dice_roll:
            reroll = randint(1,6)
            matches += 1
        match matches:
            case 0:
                low, high = 5, 50
            case 1:
                low, high = 50, 100
            case 2: 
                low, high = 100, 200
            case _:
                low, high = 200, 500
        
        bet: int = randint(low, high) 

        mod_value: int = bet % 5

        if mod_value < 3:
            bet = bet - mod_value 
        else:
            bet = bet + (5 - mod_value)

        return bet

    def setStatus(self, over: bool) -> None:
        self.over: bool = over

    def createHand(self) -> None:
        new_hand: Hand = Hand()
        self.hands.append(new_hand)

    def affinityUp(self) -> None:
        self.affinity += 1
    
    def affinityDown(self) -> None:
        self.affinity -= 1

    def hasTwentyOne(self, hand: Hand) -> bool:
        end_string: str = ""
        player_type_str: str = ""
        hand_length: int = len(hand.cards)
        has_twenty_one: bool = hand.count_hand() == 21

        # If player has 21 stand automatically
        if has_twenty_one:
            self.setStatus(False)

            match hand_length:
                case 2:
                    end_string = "got blackjack!"
                case _:
                    end_string = "got 21!"

            if isinstance(self, Player):
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
    
    def isOver(self) -> bool:
        overMessage: str = ''
        for hand in self.hands:
            if hand.count_hand() > 21:
                self.setStatus(True)

                if isinstance(self, Player) and not isinstance(self, Dealer):
                    match self.type:
                        case "player":
                            overMessage = 'You busted!'
                        case __:
                            overMessage = f'{self.player_name} busted!'
                    self.money -= self.bet
                else:
                    overMessage = 'The dealer busted!'

                print(overMessage)
                return True
            
        return False

class Dealer(Player):
    def __init__(self, id: str, deck: Deck, hand: Hand) -> None:
        self.id: str = id
        self.deck: Deck = deck
        self.hands: list[Hand] = [hand]

    def deal_card(self, hand:Hand) -> Card:
        dealt_card: Card = self.deck.cards.pop(0)
        hand.add_card(dealt_card)
        return dealt_card
    
    def burn_card(self) -> None:
        self.deck.cards.pop(0)
    
    def deal_self(self) -> None:
        self.hands[0].add_card(self.deck.cards.pop(0))

    def get_dealer_up_card(self) -> Card:
        return self.hands[0].cards[1]


class Table:
    def __init__(self, dealer: Dealer) -> None:
        self.table_seats: list[Union[Player, None]] = []
        self.minimum_bet: int = 0
        self.dealer: Dealer = dealer

    def getOpenSeats(self) -> list[int]:
        open_seat_indexes: list[int] = []
        for i, player in enumerate(self.table_seats):
            if player is None:
                open_seat_indexes.append(i)
        return open_seat_indexes
    
    def printTablePlayers(self, table_number) -> None:
        print(f'There are {self.getNumOpenSeats()} seat(s) available at table {table_number+1}:\n')
        print(f'People currently at table {table_number+1}:\n')
        for player in self.table_seats:
            if player is not None:
                print(f'{player.player_name}')
        print()

    def getNumOpenSeats(self) -> int:
        open_seat_count: int = 0
        for player in self.table_seats:
            if player is not None:
                open_seat_count += 1
        return open_seat_count


class Casino:
    def __init__(self, num_tables: int) -> None:
        self.num_tables: int = num_tables
        self.tables: list[Table] = []
    
    def getTable(self, table_number: int) -> Table:
        return self.tables[table_number - 1]
    
    def getTables(self) -> list[Table]:
        return self.tables
    
    def addTable(self, table: Table) -> None:
        self.tables.append(table)
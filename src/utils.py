"""Module with helper functions."""
import logging
from logging.handlers import RotatingFileHandler
import random

from src import constants


LOG = logging.getLogger()
LOG.setLevel(logging.INFO)
handler = RotatingFileHandler(constants.LOG_FILE_NAME, maxBytes=2000000, backupCount=2)
handler.setLevel(logging.INFO)
LOG.addHandler(handler)


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        if self.rank <= 10:
            return f"{self.rank}({self.suit})"
        else:
            return f"{constants.rank_face_mapping[self.rank]}({self.suit})"
        

def log(message: str) -> None:
    """Logs a message.

    Prepends the message with 'log:' so that logs associated with a game can be filtered.

    Parameters:
        message (str): Message to log
    """
    LOG.info(f"log:{message}")


def build_response(game_id: str, winner: str = None) -> dict:
    """Builds the response dictionary for a game.
    
    Inserts the associated ID for the game and the result of the game.
    
    Parameters:
        game_id (str): UUID of the game
        winner (str|None): If there is a winner, it will insert the name of the player. If not, it inserts a message

    Returns:
        Response dictionary
    """
    if not winner:
        return {
            constants.GAME_ID: game_id,
            constants.RESULT: "No result! Stopped game after 2000 turns!"
        }
    return {
            constants.GAME_ID: game_id,
            constants.RESULT: winner
        }
        

def get_deck_of_cards():
    """Generates a deck of 52 cards and returns them as a list.
    """
    cards = list()
    for rank in constants.ranks:
        for suit in constants.suits:
            card = Card(suit, rank)
            cards.append(card)
    return cards


def shuffle_and_deal_cards(cards: list) -> tuple:
    """Shuffles the deck of cards and deals it equally to both players.

    Each player will end up with 26 cards.

    Parameters:
        cards (list): A list of 52 card objects
    
    Returns:
        A tuple of first and second players' cards - 26 each
    """
    random.shuffle(cards)
    player1_cards = cards[0::2]
    player2_cards = cards[1::2]
    return player1_cards, player2_cards


def draw_card(hand: list, number: int = 1) -> tuple:
    """Draws the specified number of cards and returns a tuple of drawn and remaining cards.
    
    If number=1, it signifies drawing one card and placing it face up.
    If number=2, it signifies drawing two cards - one face down and one face up.

    Parameters:
        hand (list): A list of cards for a player
        number (int): The number of cards to draw
    
    Returns:
        A tuple of the drawn cards and the cards left with the player
    """
    return hand[:number], hand[number:]
    

def go_to_war(state_of_game: dict, player1_name: str, player2_name: str) -> tuple:
    """Simulates when two players go to war (face-up cards have the same rank).

    If two players get a face-up card with the same rank, they will put down one face-down card and one face-up card.
    The face-up card will compete.
    This continues as long as the face-up card has the same rank.

    Parameters:
        state_of_game (dict): A dictionary containing each player's current drawn cards and their remaining cards
        player1_name (str): The name of player 1
        player2_name (str): The name of player 2
    
    Returns:
        A tuple of player 1 and player 2's remaining cards
    """
    cards_in_play = list()

    player1_cards = state_of_game[constants.PLAYER1_CARDS]
    player2_cards = state_of_game[constants.PLAYER2_CARDS]
    player1_hand =  state_of_game[constants.PLAYER1_HAND] 
    player2_hand = state_of_game[constants.PLAYER2_HAND]
    turns = state_of_game[constants.TURNS]

    cards_in_play.extend(player1_cards)
    cards_in_play.extend(player2_cards)

    while (player1_hand or player2_hand) and player1_cards[-1].rank == player2_cards[-1].rank:
        turns -= 1
        log(f"{player1_name}'s card and {player2_name}'s card have the same rank")
        log("WAR!")
        if player1_hand:
            player1_cards, player1_hand = draw_card(player1_hand, 2)
            cards_in_play.extend(player1_cards)
        log(f"{player1_name}'s card: {player1_cards[-1]}")
        if player2_hand:
            player2_cards, player2_hand = draw_card(player2_hand, 2)
            cards_in_play.extend(player2_cards)
        log(f"{player2_name}'s card: {player2_cards[-1]}")

    if player2_cards[-1].rank > player1_cards[-1].rank:
        player2_hand.extend(cards_in_play)
        log(f"{player2_name}'s card has a higher rank")
    elif player1_cards[-1].rank > player2_cards[-1].rank:
        player1_hand.extend(cards_in_play)
        log(f"{player1_name}'s card has a higher rank")
    else:
        log(f"{player1_name}'s card and {player2_name}'s card have the same rank")

    log(f"{player1_name} now has {len(player1_hand)} cards")
    log(f"{player2_name} now has {len(player2_hand)} cards")

    return player1_hand, player2_hand, turns

"""Module with the functions associated with a game."""
import re
import uuid

from src import constants
from src.utils import build_response
from src.utils import draw_card
from src.utils import get_deck_of_cards
from src.utils import go_to_war
from src.utils import log
from src.utils import shuffle_and_deal_cards
import src.wins as wins


def start_new_game(player1: str, player2: str) -> dict:
    """Starts a new game between two players and returns the result of the game.
    
    Parameters:
        player1 (str): Name of Player 1
        player2 (str): Name of Player 2

    Returns:
        A response dictionary with the game ID and the result of the game 
    """
    game_id = str(uuid.uuid4().hex)
    log(f"Gameid:{game_id}")

    deck_of_cards = get_deck_of_cards()
    player1_hand, player2_hand = shuffle_and_deal_cards(deck_of_cards)
    turns = 2000

    while player1_hand and player2_hand:
        turns -= 1
        if turns <= 0:
            break

        player1_cards, player1_hand = draw_card(player1_hand)
        log(f"{player1}'s card: {player1_cards[-1]}")
        player2_cards, player2_hand = draw_card(player2_hand)
        log(f"{player2}'s card: {player2_cards[-1]}")

        if player2_cards[-1].rank > player1_cards[-1].rank:
            player2_hand.append(player1_cards[-1])
            player2_hand.append(player2_cards[-1])

            log(f"{player2}'s card has a higher rank")
            log(f"{player1} now has {len(player1_hand)} cards")
            log(f"{player2} now has {len(player2_hand)} cards")

        elif player1_cards[-1].rank > player2_cards[-1].rank:
            player1_hand.append(player1_cards[-1])
            player1_hand.append(player2_cards[-1])

            log(f"{player1}'s card has a higher rank")
            log(f"{player1} now has {len(player1_hand)} cards")
            log(f"{player2} now has {len(player2_hand)} cards")

        else:
            state_of_game = {
                constants.PLAYER1_CARDS: player1_cards,
                constants.PLAYER2_CARDS: player2_cards,
                constants.PLAYER1_HAND: player1_hand,
                constants.PLAYER2_HAND: player2_hand,
                constants.TURNS: turns
            }
            player1_hand, player2_hand, turns = go_to_war(state_of_game, player1, player2)

    if turns <= 0:
        log("More than 2000 turns played with no result; exiting")

        return build_response(game_id)
    
    else:
        if not player1_hand and not player2_hand:
            log(f"{player1} and {player2} drew the game!")

            return build_response(game_id, winner=f"{player1} and {player2} drew the game!")
        
        if not player1_hand:
            log(f"{player2} won!")
            wins.update_db(player2)

            return build_response(game_id, winner=player2)
        
        if not player2_hand:
            log(f"{player1} won!")
            wins.update_db(player1)

            return build_response(game_id, winner=player1)


def get_game_logs(game_id: str) -> list:
    """Retrieves logs associated with a game.
    
    Parameters:
        game_id (str): Game for which to get logs

    Returns:
        A list containing the game logs
    """
    logs = []
    with open(constants.LOG_FILE_NAME, "r") as file:
        lines = file.readlines()
    
    i = 0
    while i < len(lines):
        if lines[i].strip() == f"log:Gameid:{game_id}":
            break
        i += 1        
    i += 1
    while i < len(lines):
        if "Gameid" in lines[i]:
            break
        match = re.match("log:(.*)", lines[i])
        if match:
            logs.append(match.group(1))
        i += 1
    return logs

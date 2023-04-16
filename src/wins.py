"""Module with the CRUD operations for the database."""
from typing import Union

from config import db
from models import Win
from models import win_schema


def update_db(player_name: str) -> win_schema:
    """Updates the database by either creating an entry for the player or updating the player's win count.

    Parameters:
        player_name (str): Player name for which to create/update entry
    
    Returns:
        The win schema with the player's entry
    """
    existing_person = db.session.query(Win).filter_by(playerName=player_name).first()

    if existing_person is None:
        new_person = win_schema.load(dict(playerName=player_name, wins=1), session=db.session)
        db.session.add(new_person)
        db.session.commit()
        return win_schema.dump(new_person), 201
    else:
        existing_person.wins = existing_person.wins + 1
        db.session.merge(existing_person)
        db.session.commit()
        return win_schema.dump(existing_person), 201
        

def read_one(player_name: str):
    """Reads the entry of the player from the database.
    
    If the player does not exist in the database, it returns an entry with 0 wins.
    
    Parameters:
        player_name (str): Player name for which to create/update entry
    
    Returns:
        The win schema with the requested player or a dictionary with the player and 0 wins.
    """
    player = db.session.query(Win).filter_by(playerName=player_name).first()

    if player is not None:
        return win_schema.dump(player)
    else:
        return {'player_name': player_name, 'wins': 0}, 201

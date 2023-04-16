"""Module with constants used in the war game application."""
GAME_ID = "game_id"
LOG_FILE_NAME = "game_logs.log"
PLAYER1_CARDS = "player1_cards"
PLAYER1_HAND = "player1_hand"
PLAYER2_CARDS = "player2_cards"
PLAYER2_HAND = "player2_hand"
RESULT = "result"
TURNS = "turns"

ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
rank_face_mapping = {
    11: "jack",
    12: "queen",
    13: "king",
    14: "ace"
}
suits = ["hearts", "diamonds", "spades", "clubs"]

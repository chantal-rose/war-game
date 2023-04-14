from unittest import mock, TestCase

from src import constants
from src import utils


class TestCardClass(TestCase):
    def test_init_not_face(self):
        card = utils.Card("diamonds", 1)
        assert card.rank == 1
        assert card.suit == "diamonds"
        assert str(card) == "1(diamonds)"
    
    def test_init_face(self):
        card = utils.Card("diamonds", 14)
        assert card.rank == 14
        assert card.suit == "diamonds"
        assert str(card)  == "ace(diamonds)"

    def test_get_deck_of_cards(self):
        assert len(utils.get_deck_of_cards()) == 52


@mock.patch.object(utils, "LOG")
def test_log(mock_log):
    log_message = "Log Message"
    utils.log(log_message)
    mock_log.info.assert_called_with(f"log:{log_message}")

def test_build_response_no_winner():
    assert utils.build_response("sample_id") == {constants.GAME_ID: "sample_id",
                                                 constants.RESULT: "No result! Stopped game after 2000 turns!"}


def test_build_response_winner():
    assert utils.build_response("sample_id", winner="sample player") == {constants.GAME_ID: "sample_id",
                                                                         constants.RESULT: "sample player"}

def test_shuffle_and_deal_cards():
    list1, list2 = utils.shuffle_and_deal_cards([1, 2, 3, 4, 5, 6, 7, 8])
    assert set(list1).intersection(list2) == set()

def test_draw_card():
    assert utils.draw_card([1,2,3,4]) == ([1], [2,3,4])

def test_draw_card_multiple():
    assert utils.draw_card([1,2,3,4], 2) == ([1,2], [3, 4])


@mock.patch.object(utils, "log")
def test_war_one_round(mock_log):
    mock_player_1_cards, mock_player_2_cards = [mock.MagicMock(rank=2)], [mock.MagicMock(rank=2)]
    mock_player_1_hand = [mock.MagicMock(rank=4), mock.MagicMock(rank=3), mock.MagicMock(rank=6)]
    mock_player_2_hand = [mock.MagicMock(rank=3), mock.MagicMock(rank=6), mock.MagicMock(rank=4)]
    state_of_game = {
                constants.PLAYER1_CARDS: mock_player_1_cards,
                constants.PLAYER2_CARDS: mock_player_2_cards,
                constants.PLAYER1_HAND: mock_player_1_hand,
                constants.PLAYER2_HAND: mock_player_2_hand,
                constants.TURNS: 3
            }
    player1_hand_result, player2_hand_result, turns = utils.go_to_war(state_of_game, "player1", "player2")
    assert len(player2_hand_result) == 7
    assert len(player1_hand_result) == 1


@mock.patch.object(utils, "log")
def test_war_multiple_rounds(mock_log):
    mock_player_1_cards, mock_player_2_cards = [mock.MagicMock(rank=2)], [mock.MagicMock(rank=2)]
    mock_player_1_hand = [mock.MagicMock(rank=4), mock.MagicMock(rank=3), mock.MagicMock(rank=6),  mock.MagicMock(rank=5)]
    mock_player_2_hand = [mock.MagicMock(rank=3), mock.MagicMock(rank=3), mock.MagicMock(rank=4)]
    state_of_game = {
                constants.PLAYER1_CARDS: mock_player_1_cards,
                constants.PLAYER2_CARDS: mock_player_2_cards,
                constants.PLAYER1_HAND: mock_player_1_hand,
                constants.PLAYER2_HAND: mock_player_2_hand,
                constants.TURNS: 3
            }
    player1_hand_result, player2_hand_result, turns = utils.go_to_war(state_of_game, "player1", "player2")
    assert len(player2_hand_result) == 0
    assert len(player1_hand_result) == 9


@mock.patch.object(utils, "log")
def test_war_cards_over_during_war_wins(mock_log):
    mock_player_1_cards, mock_player_2_cards = [mock.MagicMock(rank=2)], [mock.MagicMock(rank=2)]
    mock_player_1_hand = [mock.MagicMock(rank=4), mock.MagicMock(rank=3), mock.MagicMock(rank=6),  mock.MagicMock(rank=1), mock.MagicMock(rank=8)]
    mock_player_2_hand = [mock.MagicMock(rank=3), mock.MagicMock(rank=3)]
    state_of_game = {
                constants.PLAYER1_CARDS: mock_player_1_cards,
                constants.PLAYER2_CARDS: mock_player_2_cards,
                constants.PLAYER1_HAND: mock_player_1_hand,
                constants.PLAYER2_HAND: mock_player_2_hand,
                constants.TURNS: 3
            }
    player1_hand_result, player2_hand_result, turns = utils.go_to_war(state_of_game, "player1", "player2")
    assert len(player2_hand_result) == 8
    assert len(player1_hand_result) == 1


@mock.patch.object(utils, "log")
def test_war_cards_over_during_war_loses(mock_log):
    mock_player_1_cards, mock_player_2_cards = [mock.MagicMock(rank=2)], [mock.MagicMock(rank=2)]
    mock_player_1_hand = [mock.MagicMock(rank=4), mock.MagicMock(rank=3), mock.MagicMock(rank=6),  mock.MagicMock(rank=5)]
    mock_player_2_hand = [mock.MagicMock(rank=3), mock.MagicMock(rank=3)]
    state_of_game = {
                constants.PLAYER1_CARDS: mock_player_1_cards,
                constants.PLAYER2_CARDS: mock_player_2_cards,
                constants.PLAYER1_HAND: mock_player_1_hand,
                constants.PLAYER2_HAND: mock_player_2_hand,
                constants.TURNS: 3
            }
    player1_hand_result, player2_hand_result, turns = utils.go_to_war(state_of_game, "player1", "player2")
    assert len(player2_hand_result) == 0
    assert len(player1_hand_result) == 8


@mock.patch.object(utils, "log")
def test_war_draw(mock_log):
    mock_player_1_cards, mock_player_2_cards = [mock.MagicMock(rank=2)], [mock.MagicMock(rank=2)]
    mock_player_1_hand = []
    mock_player_2_hand = []
    state_of_game = {
                constants.PLAYER1_CARDS: mock_player_1_cards,
                constants.PLAYER2_CARDS: mock_player_2_cards,
                constants.PLAYER1_HAND: mock_player_1_hand,
                constants.PLAYER2_HAND: mock_player_2_hand,
                constants.TURNS: 3
            }
    player1_hand_result, player2_hand_result, turns = utils.go_to_war(state_of_game, "player1", "player2")
    assert len(player2_hand_result) == 0
    assert len(player1_hand_result) == 0
from unittest import mock
import uuid

from src import game


MOCK_LOGS = "Ignored line\nlog:Gameid:{}\nlog:First line\nlog:Second line\nlog:Gameid:123"
MOCK_PLAYER_1_HAND = [mock.MagicMock(rank=2),
                      mock.MagicMock(rank=8),
                      mock.MagicMock(rank=6),
                      mock.MagicMock(rank=1),
                      mock.MagicMock(rank=1)]
MOCK_PLAYER_2_HAND = [mock.MagicMock(rank=3),
                      mock.MagicMock(rank=4),
                      mock.MagicMock(rank=6),
                      mock.MagicMock(rank=1),
                      mock.MagicMock(rank=1)]


@mock.patch.object(game, "build_response")
@mock.patch.object(game.wins, "update_db")
@mock.patch.object(game, "go_to_war")
@mock.patch.object(game, "draw_card")
@mock.patch.object(game, "shuffle_and_deal_cards")
@mock.patch.object(game, "get_deck_of_cards")
@mock.patch.object(game, "uuid")
@mock.patch.object(game, "log")
def test_start_game_player2_wins(mock_log,
                                 mock_uuid,
                                 mock_get_deck_of_cards,
                                 mock_shuffle,
                                 mock_draw_card,
                                 mock_go_to_war,
                                 mock_update_db,
                                 mock_build_response):
    mock_uuid.uuid4.return_value.hex = "test_uuid"
    mock_shuffle.return_value = (MOCK_PLAYER_1_HAND[:1], MOCK_PLAYER_2_HAND[:1])
    mock_draw_card.side_effect = [(MOCK_PLAYER_1_HAND[:1], []), (MOCK_PLAYER_2_HAND[:1], [])]
    game.start_new_game("player1", "player2")
    mock_build_response.assert_called_with("test_uuid", winner="player2")
    assert not mock_go_to_war.called
    mock_update_db.assert_called_with("player2")


@mock.patch.object(game, "build_response")
@mock.patch.object(game.wins, "update_db")
@mock.patch.object(game, "go_to_war")
@mock.patch.object(game, "draw_card")
@mock.patch.object(game, "shuffle_and_deal_cards")
@mock.patch.object(game, "get_deck_of_cards")
@mock.patch.object(game, "uuid")
@mock.patch.object(game, "log")
def test_start_game_player1_wins(mock_log,
                                 mock_uuid,
                                 mock_get_deck_of_cards,
                                 mock_shuffle,
                                 mock_draw_card,
                                 mock_go_to_war,
                                 mock_update_db,
                                 mock_build_response):
    mock_uuid.uuid4.return_value.hex = "test_uuid"
    mock_shuffle.return_value = (MOCK_PLAYER_1_HAND[1:2], MOCK_PLAYER_2_HAND[1:2])
    mock_draw_card.side_effect = [(MOCK_PLAYER_1_HAND[1:2], []), (MOCK_PLAYER_2_HAND[1:2], [])]
    game.start_new_game("player1", "player2")
    mock_build_response.assert_called_with("test_uuid", winner="player1")
    assert not mock_go_to_war.called
    mock_update_db.assert_called_with("player1")


@mock.patch.object(game, "build_response")
@mock.patch.object(game.wins, "update_db")
@mock.patch.object(game, "go_to_war")
@mock.patch.object(game, "draw_card")
@mock.patch.object(game, "shuffle_and_deal_cards")
@mock.patch.object(game, "get_deck_of_cards")
@mock.patch.object(game, "uuid")
@mock.patch.object(game, "log")
def test_start_game_war(mock_log, 
                        mock_uuid,
                        mock_get_deck_of_cards,
                        mock_shuffle,
                        mock_draw_card,
                        mock_go_to_war,
                        mock_update_db,
                        mock_build_response):
    mock_uuid.uuid4.return_value.hex = "test_uuid"
    mock_shuffle.return_value = (MOCK_PLAYER_1_HAND, MOCK_PLAYER_2_HAND)
    mock_draw_card.side_effect = [(MOCK_PLAYER_1_HAND[2:3], MOCK_PLAYER_1_HAND[3:]),
                                  (MOCK_PLAYER_2_HAND[2:3], MOCK_PLAYER_2_HAND[3:]),
                                  (MOCK_PLAYER_1_HAND[:1], []),
                                  (MOCK_PLAYER_2_HAND[:1], [])]
    mock_go_to_war.return_value = (MOCK_PLAYER_1_HAND[:1], MOCK_PLAYER_2_HAND[:1], 100)
    game.start_new_game("player1", "player2")
    mock_build_response.assert_called_with("test_uuid", winner="player2")
    assert mock_go_to_war.called
    mock_update_db.assert_called_with("player2")


@mock.patch.object(game, "build_response")
@mock.patch.object(game.wins, "update_db")
@mock.patch.object(game, "go_to_war")
@mock.patch.object(game, "draw_card")
@mock.patch.object(game, "shuffle_and_deal_cards")
@mock.patch.object(game, "get_deck_of_cards")
@mock.patch.object(game, "uuid")
@mock.patch.object(game, "log")
def test_start_game_two_wars_and_draw(mock_log,
                                      mock_uuid,
                                      mock_get_deck_of_cards,
                                      mock_shuffle,
                                      mock_draw_card,
                                      mock_go_to_war,
                                      mock_update_db,
                                      mock_build_response):
    mock_uuid.uuid4.return_value.hex = "test_uuid"
    mock_shuffle.return_value = (MOCK_PLAYER_1_HAND, MOCK_PLAYER_2_HAND)
    mock_draw_card.side_effect = [(MOCK_PLAYER_1_HAND[2:3], MOCK_PLAYER_1_HAND[3:]),
                                  (MOCK_PLAYER_2_HAND[2:3], MOCK_PLAYER_2_HAND[3:]),
                                  (MOCK_PLAYER_1_HAND[3:4], []),
                                  (MOCK_PLAYER_2_HAND[3:4], [])]
    mock_go_to_war.side_effect = [(MOCK_PLAYER_1_HAND[3:4], MOCK_PLAYER_2_HAND[3:4], 100),
                                  ([], [], 100)]
    game.start_new_game("player1", "player2")
    mock_build_response.assert_called_with("test_uuid", winner="player1 and player2 drew the game!")
    assert mock_go_to_war.call_count == 2
    assert not mock_update_db.called


@mock.patch.object(game, "build_response")
@mock.patch.object(game.wins, "update_db")
@mock.patch.object(game, "go_to_war")
@mock.patch.object(game, "draw_card")
@mock.patch.object(game, "shuffle_and_deal_cards")
@mock.patch.object(game, "get_deck_of_cards")
@mock.patch.object(game, "uuid")
@mock.patch.object(game, "log")
def test_start_game_no_more_turns(mock_log,
                                  mock_uuid,
                                  mock_get_deck_of_cards,
                                  mock_shuffle,
                                  mock_draw_card,
                                  mock_go_to_war,
                                  mock_update_db,
                                  mock_build_response):
    mock_uuid.uuid4.return_value.hex = "test_uuid"
    mock_shuffle.return_value = (MOCK_PLAYER_1_HAND, MOCK_PLAYER_2_HAND)
    mock_draw_card.side_effect = [(MOCK_PLAYER_1_HAND[2:3], MOCK_PLAYER_1_HAND[3:]),
                                  (MOCK_PLAYER_2_HAND[2:3], MOCK_PLAYER_2_HAND[3:])]
    mock_go_to_war.return_value = (MOCK_PLAYER_1_HAND[:1], MOCK_PLAYER_2_HAND[:1], 0)
    game.start_new_game("player1", "player2")
    mock_build_response.assert_called_with("test_uuid")
    assert mock_go_to_war.call_count == 1
    assert not mock_update_db.called


def test_get_game_logs():
    test_uuid = str(uuid.uuid4().hex)
    with mock.patch('src.game.open', mock.mock_open(read_data=MOCK_LOGS.format(test_uuid))) as mocked_file:
        lines = game.get_game_logs(test_uuid)
        assert lines == ["First line", "Second line"]
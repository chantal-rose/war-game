from unittest import mock

from src import wins


@mock.patch.object(wins, "db")
def test_update_db_doesnt_exist(mock_db):
    mock_query = mock.Mock()
    mock_db.session.query.return_value = mock_query
    mock_filter = mock.Mock()
    mock_query.filter_by.return_value = mock_filter
    mock_filter.first.return_value = None
    wins.update_db("player1")


@mock.patch.object(wins, "win_schema")
@mock.patch.object(wins, "db")
def test_update_db_exists(mock_db, mock_schema):
    mock_query = mock.Mock()
    mock_db.session.query.return_value = mock_query
    mock_filter = mock.Mock()
    mock_query.filter_by.return_value = mock_filter
    mock_existing_person = mock.MagicMock(wins=2)
    mock_filter.first.return_value = mock_existing_person
    wins.update_db("player1")
    mock_existing_person.wins = 3
    mock_schema.dump.assert_called_with(mock_existing_person)


@mock.patch.object(wins, "win_schema")
@mock.patch.object(wins, "db")
def test_read_one_exists(mock_db, mock_schema):
    mock_query = mock.Mock()
    mock_db.session.query.return_value = mock_query
    mock_filter = mock.Mock()
    mock_query.filter_by.return_value = mock_filter
    mock_existing_person = mock.MagicMock(player_name="player1", wins=2)
    mock_filter.first.return_value = mock_existing_person
    wins.read_one("player1")
    mock_schema.dump.assert_called_with(mock_existing_person)


@mock.patch.object(wins, "win_schema")
@mock.patch.object(wins, "db")
def test_read_one_doesnt_exist(mock_db, mock_schema):
    mock_query = mock.Mock()
    mock_db.session.query.return_value = mock_query
    mock_filter = mock.Mock()
    mock_query.filter_by.return_value = mock_filter
    mock_filter.first.return_value = None
    assert wins.read_one("player1") == ({'player_name': "player1", 'wins': 0}, 201)

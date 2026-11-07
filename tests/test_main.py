from unittest.mock import patch, MagicMock
import requests
import main
import pytest
from main import add_film_to_library, add_films

@pytest.fixture(autouse=True)
def no_menu_prompt():
    with patch("main.return_to_menu", return_value=None):
        yield

# @patch("main.requests.post")
# def test_returns_title_on_success(mock_post):
#     mock_post.return_value = MagicMock(status_code=200)

#     assert add_film_to_library("Memento") == "Memento"


# @patch("main.requests.post")
# def test_sends_correct_request(mock_post):
#     mock_post.return_value = MagicMock(status_code=200)

#     add_film_to_library("Memento", watched=True)

#     mock_post.assert_called_once_with(
#         f"{main.base_url}/api/all/watched_film",
#         json={"title": "Memento", "watched": True},
#     )


# @patch("main.requests.post")
# def test_returns_none_on_error_status(mock_post, capsys):
#     mock_post.return_value = MagicMock(
#         status_code=409,
#         json=lambda: {"error": "Memento is already in your library"},
#     )

#     assert add_film_to_library("Memento") is None
#     assert "already in your library" in capsys.readouterr().out


# @patch("main.requests.post")
# def test_returns_none_when_request_fails(mock_post, capsys):
#     mock_post.side_effect = requests.exceptions.RequestException

#     assert add_film_to_library("Memento") is None
#     assert "issue with your post request" in capsys.readouterr().out
patch("main.add_film_to_library", return_value="Memento")
@patch("builtins.input", return_value="memento")
def test_add_films_success_sets_current_film(mock_input, mock_add, capsys):
    main.current_film = None

    add_films()

    mock_add.assert_called_once_with("memento", watched=True)
    assert "has been added to your tracked films" in capsys.readouterr().out


@patch("main.add_film_to_library", return_value=None)
@patch("builtins.input", return_value="memento")
def test_add_films_failure_returns_to_menu(mock_input, mock_add, capsys):
    assert add_films() is None
    assert "Going back to the Main Menu" in capsys.readouterr().out


@patch("main.add_film_to_library", return_value="Memento")
@patch("builtins.input", return_value="memento")
def test_add_films_success_sets_current_film(mock_input, mock_add, capsys):
    main.current_film = None

    add_films()

    mock_add.assert_called_once_with("memento", watched=True)
    assert "has been added to your tracked films" in capsys.readouterr().out

@patch("main.add_film_to_library")
@patch("builtins.input", return_value="")
def test_add_films_empty_title_is_not_posted(mock_input, mock_add, capsys):
    add_films()

    assert "Please enter a film title" in capsys.readouterr().out
    mock_add.assert_not_called()
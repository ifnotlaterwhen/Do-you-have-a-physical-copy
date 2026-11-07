from unittest.mock import patch

import mysql.connector
import pytest
import requests

with patch("DButils.FilmDB"), patch("config.DB_manager"):
    from app import app, search_tmdb

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_missing_title_returns_400(client):
    response = client.post("/api/all/watched_film", json={})
    assert response.status_code == 400


@patch("app.dbutils")
@patch("app.search_tmdb")
def test_new_film_is_saved(mock_search, mock_dbutils, client):
    film = {
        "tmdb_id": 77,
        "title": "Memento",
        "overview": "Plot",
        "genres": ["Thriller"],
        "directors": ["Christopher Nolan"],
        "actors": ["Guy Pearce"]
    }
    mock_search.return_value = film
    mock_dbutils.fetch_all_movies.return_value = [("Inception",)]

    response = client.post("/api/all/watched_film", json={"title": "memento"})

    assert response.status_code == 200
    assert response.get_json() == {"title": "Memento", "watched": True}
    mock_dbutils.new_watched_film.assert_called_once_with(film)


@patch("app.dbutils")
@patch("app.search_tmdb")
def test_duplicate_returns_409(mock_search, mock_dbutils, client):
    mock_search.return_value = {"id": 27205, "title": "Inception", "overview": "x"}
    mock_dbutils.fetch_all_movies.return_value = [("Inception",)]

    response = client.post("/api/all/watched_film", json={"title": "incepton"})

    assert response.status_code == 409
    mock_dbutils.new_watched_film.assert_not_called()


@patch("app.search_tmdb")
def test_film_not_on_tmdb_returns_404(mock_search, client):
    mock_search.return_value = None
    response = client.post("/api/all/watched_film", json={"title": "zzzz"})
    assert response.status_code == 404


@patch("app.search_tmdb")
def test_tmdb_down_returns_502(mock_search, client):
    mock_search.side_effect = requests.exceptions.RequestException
    response = client.post("/api/all/watched_film", json={"title": "Memento"})
    assert response.status_code == 502


@patch("app.dbutils")
@patch("app.search_tmdb")
def test_database_error_returns_500(mock_search, mock_dbutils, client):
    mock_search.return_value = {"id": 77, "title": "Memento", "overview": "x"}
    mock_dbutils.fetch_all_movies.return_value = []
    mock_dbutils.new_watched_film.side_effect = mysql.connector.Error("db down")

    response = client.post("/api/all/watched_film", json={"title": "Memento"})

    assert response.status_code == 500

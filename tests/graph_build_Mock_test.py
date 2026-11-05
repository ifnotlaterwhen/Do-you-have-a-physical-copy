from graph import Graph
from graph_build import GraphBuild
from unittest.mock import patch, MagicMock

FAKE_DATA = [
    {
        "title": "Inception",
        "genres": "Action, Sci-Fi",
        "directors": "Christopher Nolan",
        "actors": "Leonardo DiCaprio",
    },
    {
        "title": "Interstellar",
        "genres": "Sci-Fi, Adventure",
        "directors": "Christopher Nolan",
        "actors": "Matthew McConaughey",
    },

    {
        "title": "The Matrix",
        "genres": "Action, Crime, Thriller",
        "directors": "Lana Wachowski, Lilly Wachowski",
        "actors": "KeanuReeves",
    },
    {
        "title": "Dune Part 2",
        "genres": "Action, Adventure, Sci-Fi",
        "directors": "Christopher Nolan",
        "actors": "Timothée Chalamet",
    },
{
        "title": "Spirited Away",
        "genres": "Action, Animation",
        "directors": "Hayao Miyazaki",
        "actors": "Rumi Hiiragi",
    },
{
        "title": "Parasite",
        "genres": "Crime ,Drama, Thriller",
        "directors": "Bong Joon-ho",
        "actors": "Song Kang-ho",
    },
]

def test_build():
    mock_db = MagicMock()
    mock_db.fetch_info_for_graph.return_value = FAKE_DATA

    graph = GraphBuild(Graph(), mock_db).build()

    inception = graph.adjacency["Movie:Inception"]
    assert "Actor:Leonardo DiCaprio" in inception
    assert "Director:Christopher Nolan" in inception
    assert "Genre:Action" in inception
    assert "Genre:Sci-Fi" in inception

    interstellar = graph.adjacency["Movie:Interstellar"]
    assert "Director:Christopher Nolan" in interstellar
    assert "Actor:Matthew McConaughey" in interstellar
    assert "Genre:Sci-Fi" in interstellar
    assert "Genre:Adventure" in interstellar
    assert "Genre:Sci-Fi" in interstellar

    mock_db.fetch_info_for_graph.assert_called_once()


def test_dfs():
    mock_db = MagicMock()
    mock_db.fetch_info_for_graph.return_value = FAKE_DATA

    builder = GraphBuild(Graph(), mock_db)
    builder.build()

    genre, people = builder.dfs("Movie:Inception")

    assert genre == {
        "Genre:Action": 4

    }
    assert people == {
        "Director:Christopher Nolan": 6,
    }
def test_movie_titles(mocker):
        graph = mocker.MagicMock()
        graph.adjacency = {
            "Movie:Inception": {"Actor:Leonardo DiCaprio", "Genre:Action"},
            "Movie:Memento": {"Director:Christopher Nolan"},
            "Actor:Leonardo DiCaprio": {"Movie:Inception"},
            "Director:Christopher Nolan": {"Movie:Memento"},
            "Genre:Action": {"Movie:Inception"},
        }

        movies = GraphBuild(graph, mocker.MagicMock())
        result = movies.movie_titles()

        assert result == {"Inception", "Memento"}
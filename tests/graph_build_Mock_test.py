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
        "genres": "Sci-Fi, Drama",
        "directors": "Christopher Nolan",
        "actors": "Matthew McConaughey",
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
    assert "Genre:Drama" in interstellar

    mock_db.fetch_info_for_graph.assert_called_once()


def test_build_connects_actor_to_director():
    mock_db = MagicMock()
    mock_db.fetch_info_for_graph.return_value = FAKE_DATA

    graph = GraphBuild(Graph(), mock_db).build()

    assert "Director:Christopher Nolan" in graph.adjacency["Actor:Leonardo DiCaprio"]
    assert "Actor:Leonardo DiCaprio" in graph.adjacency["Director:Christopher Nolan"]

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
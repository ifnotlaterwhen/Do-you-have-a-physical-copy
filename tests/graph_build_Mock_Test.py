from graph import Graph
from graph_build import GraphBuild
from unittest.mock import patch, MagicMock

FAKE_DATA = [
    {
        "title": "Inception",
        "genre": "Action, Sci-Fi",
        "directors": "Christopher Nolan",
        "actors": "Leonardo DiCaprio",
    },
    {
        "title": "Interstellar",
        "genre": "Sci-Fi, Drama",
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
    mock_db.fetch_info_for_graph.assert_called_once()

    interstellar = graph.adjacency["Movie:Interstellar"]
    assert "Director:Christopher Nolan" in interstellar
    assert "Actor:Matthew McConaughey" in interstellar
    assert "Genre:Sci-Fi" in interstellar
    assert "Genre:Drama" in interstellar
    mock_db.fetch_info_for_graph.assert_called_once()

def test_dfs():
    mock_graph = MagicMock()
    mock_graph.adjacency = {
        "Movie:A": {"Director:Nolan", "Actor:Leo", "Genre:Sci-Fi", "Genre:Action"},
        "Movie:B": {"Director:Nolan", "Actor:Leo", "Genre:Sci-Fi"},
        "Movie:C": {"Director:Nolan", "Actor:Leo", "Genre:Sci-Fi"},
        "Movie:D": {"Director:Nolan", "Actor:Leo", "Genre:Sci-Fi"},
        "Director:Nolan": {"Movie:A", "Movie:B", "Movie:C", "Movie:D"},
        "Actor:Leo": {"Movie:A", "Movie:B", "Movie:C", "Movie:D"},
        "Genre:Sci-Fi": {"Movie:A", "Movie:B", "Movie:C", "Movie:D"},
        "Genre:Action": {"Movie:A"},
    }

    genres, people = GraphBuild(mock_graph, MagicMock()).dfs("Movie:A")

    assert genres == {"Genre:Sci-Fi":4}
    assert people == {"Director:Nolan":4, "Actor:Leo":4}
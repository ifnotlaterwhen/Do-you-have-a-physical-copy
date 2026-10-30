from graph import Graph
from recomendation import Recommendation
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

    graph = Recommendation(Graph(), mock_db).build()

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
from graph import Graph
from recommendation import Recommendation
from unittest.mock import patch, MagicMock

FAKE_DATA = {
    "Inception": {
        "genre_name": "Action, Sci-Fi",
        "directed_name": "Christopher Nolan",
        "actor_name": "Leonardo DiCaprio",
    },
    "Interstellar": {
        "genre_name": "Sci-Fi, Drama",
        "directed_name": "Christopher Nolan",
        "actor_name": "Matthew McConaughey",
    },
    "Lady Bird": {
        "genre_name": "Comedy, Drama",
        "directed_name": "Greta Gerwig",
        "actor_name": "Saoirse Ronan",
    },
}

def test_build(self, Mocker):
    mock_db = MagicMock()
    mock_db.fetch_info_for_graph.return_value = FAKE_DATA

    graph = Recommendation(Graph(), mock_db).build()


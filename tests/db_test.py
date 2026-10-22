import pytest
from config import DB_manager
from DButils import FilmDB

@pytest.fixture
def clean_db():
    cleanDB = FilmDB("cinefiles")
    cleanDB.init_db()
    cleanDB.seed_db_mock()

def test_db_setup(clean_db):
    with DB_manager().get_connection() as db:
        with db.cursor() as cur:
            cur.execute("USE cinefiles")
            cur.execute("SHOW TABLES")
            result = cur.fetchall()
            tables = []
            for row in result:
                tables.append(row[0])
            assert ("actors"
                and "directors"
                and "film_genres"
                and "film_info"
                and "junc_actors"
                and "junc_directors"
                and "junc_genres"
                and "my_films"
                and "subscriptions") in tables
            
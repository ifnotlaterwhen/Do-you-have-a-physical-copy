import pytest
from config import DB_manager
from DButils import seedDB
from itertools import chain

@pytest.fixture
def clean_db():
    cleanDB = seedDB("cinefiles")
    cleanDB.init_db()
    cleanDB.seed_db_mock()

def test_db_setup(clean_db):
    with DB_manager().get_connection() as db:
        with db.cursor() as cur:
            cur.execute("USE cinefiles")
            cur.execute("SHOW TABLES")
            result = list(chain.from_iterable(cur.fetchall()))
            assert ("actors"
                and "directors"
                and "film_genres"
                and "film_info"
                and "junc_actors"
                and "junc_directors"
                and "junc_genres"
                and "my_films"
                and "subscriptions") in result
            
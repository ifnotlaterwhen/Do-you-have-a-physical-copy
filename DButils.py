# DButils.py handles all DB queries
from config import DB_manager
import json

class FilmDB:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.db_manager = DB_manager()

    def init_db(self):
        with self.db_manager.get_connection() as db:
            with db.cursor() as cur:
                cur.execute(f"""DROP DATABASE IF EXISTS {self.db_name}""")
                cur.execute(f"""CREATE DATABASE {self.db_name}""")
                cur.execute(f"""USE {self.db_name}""")
                cur.execute("""
                    CREATE TABLE my_films (
                        my_film_id INT PRIMARY KEY AUTO_INCREMENT,
                        watched BOOL,
                        dvd_owned BOOL,
                        bluray_owned BOOL,
                        4k_bluray_owned BOOL
                    )""")
                cur.execute("""
                    CREATE TABLE film_info (
                        film_id INT PRIMARY KEY AUTO_INCREMENT,
                        my_film_id INT,
                        api_film_TMDB_id INT,
                        title VARCHAR(100),
                        overview TEXT,
                        FOREIGN KEY(my_film_id) REFERENCES my_films(my_film_id)
                    )""")
                cur.execute("""
                    CREATE TABLE film_genres (
                        genre_id INT PRIMARY KEY AUTO_INCREMENT,
                        genre_name VARCHAR(50)
                    )""")
                cur.execute("""
                    CREATE TABLE junc_genres (
                        film_id INT,
                        genre_id INT,
                        FOREIGN KEY(film_id) REFERENCES film_info(film_id),
                        FOREIGN KEY(genre_id) REFERENCES film_genres(genre_id)
                    )""")
                cur.execute("""
                    CREATE TABLE directors (
                        director_id INT PRIMARY KEY AUTO_INCREMENT,
                        name VARCHAR(50)
                    )""")
                cur.execute("""
                    CREATE TABLE junc_directors (
                        director_id INT,
                        film_id INT,
                        FOREIGN KEY(director_id) REFERENCES directors(director_id),
                        FOREIGN KEY(film_id) REFERENCES film_info(film_id)
                    )""")
                cur.execute("""
                    CREATE TABLE actors (
                        actor_id INT PRIMARY KEY AUTO_INCREMENT,
                        name VARCHAR(50)
                    )""")
                cur.execute("""
                    CREATE TABLE junc_actors (
                        actor_id INT,
                        film_id INT,
                        FOREIGN KEY(actor_id) REFERENCES actors(actor_id),
                        FOREIGN KEY(film_id) REFERENCES film_info(film_id)
                    )""")
                cur.execute("""
                    CREATE TABLE subscriptions (
                        subscription_id INT PRIMARY KEY AUTO_INCREMENT,
                        service VARCHAR(50),
                        service_TMDB_id INT,
                        active BOOL
                    )""")
            db.commit()

    def seed_db_mock(self):
        with open("mock_data.json", "r") as f:
            data = json.load(f)
            with self.db_manager.get_connection() as db:
                with db.cursor(dictionary=True) as cur:
                    cur.execute(f"USE {self.db_name}")
                    for film in data["my_films"]:
                        cur.execute("""
                            INSERT INTO my_films (watched, dvd_owned, bluray_owned, 4k_bluray_owned)
                            VALUES
                            (%s, %s, %s,%s)""",
                            (
                                film["watched"],
                                film["dvd_owned"],
                                film["bluray_owned"],
                                film["4k_bluray_owned"]
                            ))
                    for film in data["film_info"]:
                        cur.execute("""
                            INSERT INTO film_info (my_film_id, api_film_TMDB_id, title, overview)
                            VALUES
                            (%s,%s,%s,%s)""",
                            (
                                film["my_film_id"],
                                film["api_film_TMDB_id"],
                                film["title"],
                                film["overview"]
                            ))
                    for genre in data["film_genres"]:
                        cur.execute("""
                            INSERT INTO film_genres (genre_name)
                            VALUES
                            (%s)""",
                            (
                                genre["genre_name"],
                            ))
                    for junc in data["junc_genres"]:
                        cur.execute("""
                            INSERT INTO junc_genres (film_id, genre_id)
                            VALUES
                            (%s, %s)""",(
                                junc["film_id"],
                                junc["genre_id"]
                            ))
                    for director in data["directors"]:
                        cur.execute("""
                            INSERT INTO directors (name)
                            VALUES
                            (%s)""",
                            (
                                director["name"],
                            ))
                    for junc in data["junc_directors"]:
                        cur.execute("""
                            INSERT INTO junc_directors (director_id, film_id)
                            VALUES
                            (%s,%s)""",(
                                junc["director_id"],
                                junc["film_id"]
                            ))
                    for actor in data["actors"]:
                        cur.execute("""
                            INSERT INTO actors (name)
                            VALUES
                            (%s)""",(
                                actor["name"],
                            ))
                    for junc in data["junc_actors"]:
                        cur.execute("""
                            INSERT INTO junc_actors (actor_id, film_id)
                            VALUES
                            (%s,%s)""",(
                                junc["actor_id"],
                                junc["film_id"]
                            ))
                    for sub in data["subscriptions"]:
                        cur.execute("""
                            INSERT INTO subscriptions (service, service_TMDB_id, active)
                            VALUES
                            (%s,%s,%s)""",(
                                sub["service"],
                                sub["service_TMDB_id"],
                                sub["active"]
                            ))
                db.commit()

    def fetch_all_movies(self):
        #logic here to query db
        return "yay success"

    def fetch_film_by_id(self):
        #logic to get info of one single movie
        pass

    # keep adding methods that relates to movies here.
    # We can have a separate class for subscriptions?

# ===================================================================
#                        SEE WATCHED FILMS
# ===================================================================



# ===================================================================
#                        GET RECOMMENDATION
# ===================================================================



# ===================================================================
#                          HOW TO WATCH
# ===================================================================



# ===================================================================
#                         ADD PHYSICAL COPY
# ===================================================================



# ===================================================================
#                         ADD WATCHED FILM
# ===================================================================



# ===================================================================
#                         SUBSCRIPTIONS
# ===================================================================



def run():
    test_db = FilmDB("cinefiles")
    test_db.init_db()
    test_db.seed_db_mock()

if __name__ == "__main__":
    run()

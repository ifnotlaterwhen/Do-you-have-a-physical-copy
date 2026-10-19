# DButils.py handles all DB queries
# Reese's note: I think this is where we can use OOP?

class FilmDB:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def fetch_all_movies(self):
        #logic here to query db
        return "yay success"

    def fetch_film_by_id(self):
        #logic to get info of one single movie
        pass

    # keep adding methods that relates to movies here.
    # We can have a separate class for subscriptions?
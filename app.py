from flask import Flask, jsonify
from DButils import FilmDB,SQL_query
from config import DB_manager
from tmdb_api import TMDB_api
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")


app = Flask(__name__)


# ===================================================================
#                           SEE OVERVIEW
# ===================================================================

@app.route('/api/overview')
def get_overview():
    print("in overview")
    overview = FilmDB("cinefiles").fetch_overview()
    return jsonify({"data": overview}), 200

# ===================================================================
#                        SEE WATCHED FILMS
# ===================================================================

@app.route('/api/all')
def get_all_movies():
    cinefiles = FilmDB("cinefiles")
    movies = cinefiles.fetch_all_movies() #see DButils.py
    return jsonify({"data": movies}), 200 #This is mock. ATM fetch_all_movies doesn't return anything useful

# ===================================================================
#                        GET RECOMMENDATION
# ===================================================================



# ===================================================================
#                          HOW TO WATCH
# ===================================================================
@app.route("/api/how-to-watch/<movie>")
def how_to_watch(movie: str):
    stream_info = TMDB_api("https://api.themoviedb.org/3", API_KEY) #<- should this line of code be outside the function?
    stream = stream_info.find_movie_subscription(movie)
    if stream is None:

        return jsonify({"error": "Couldn't get film data"}), 404
    return jsonify(stream)

@app.route("/api/owned-physical/<movie>", methods=["GET"])
def physical_copy(movie):
    physical = SQL_query(DB_manager())
    result = physical.owned_copies(movie)
    return jsonify(result)
# ===================================================================
#                         ADD PHYSICAL COPY
# ===================================================================

@app.route('/api/all/search')
def find_film_id():
    return jsonify({"message": "Temporary code: endpoint is working!"}), 200

@app.route('/api/all/<int:my_film_id>', methods=['PATCH'])
def update_physical():
    return jsonify({"message": "Temporary code: endpoint is working!"}), 200

# ===================================================================
#                         ADD WATCHED FILM
# ===================================================================



# ===================================================================
#                         SUBSCRIPTIONS
# ===================================================================

if __name__ == "__main__":
    app.run(debug=True, port=5000)

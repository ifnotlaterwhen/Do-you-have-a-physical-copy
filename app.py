from flask import Flask, jsonify, request
from DButils import FilmDB,SQL_query
from config import DB_manager
from tmdb_api import TMDB_api
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")


import mysql.connector

app = Flask(__name__)

dbutils = FilmDB("cinefiles")      # creates instance of FilmDB class - RB

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

@app.route('/api/all/physical', methods=['PATCH'])
def update_physical():
    try:
        data = request.json
        film = data["title"]
        physical_format = data["physical_format"]

        dbutils.add_physical_copy(film, physical_format)
        return {"message": "You've added a physical copy to your library"}, 200
    
    except mysql.connector.IntegrityError:
        return jsonify({"error": "There was a problem adding this format to your library."}), 409 # Conflict

    except ValueError:
        return jsonify({"error": "Invalid physical format"}), 400
    
    except mysql.connector.Error:
        return jsonify({"error": "There was a problem with the database"}), 500 # Internal Server Error

# @app.route('api/all/search')
# def find_film_id():
#     return jsonify({"message": "Temporary code: endpoint is working!"}), 200

# @app.route('/api/all/<int:my_film_id', methods=['PATCH'])
# def update_physical():
#     return jsonify({"message": "Temporary code: endpoint is working!"}), 200

# ===================================================================
#                         ADD WATCHED FILM
# ===================================================================



# ===================================================================
#                         SUBSCRIPTIONS
# ===================================================================

if __name__ == "__main__":
    app.run(debug=True, port=5000)

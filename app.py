from flask import Flask, jsonify, request
from DButils import FilmDB,SQL_query
from config import DB_manager
from tmdb_api import TMDB_api
import os
import requests
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")


import mysql.connector

app = Flask(__name__)

dbutils = FilmDB("cinefiles")      # creates instance of FilmDB class - RB
sql_query = SQL_query(DB_manager())     # added now that add_physical_copy in class SQL_query - RB

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

        sql_query.add_physical_copy(film, physical_format)
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

def search_tmdb(title):
    search = requests.get (f"{TMDB_BASE}/search/movie", params={"query": title, "api_key": API_KEY}, timeout=10)
    search.raise_for_status()
    results = search.json().get("results", [])
    if not results:
        return None
    return results[0]

TMDB_BASE = "https://api.themoviedb.org/3"

@app.route("/api/all/film_info")
def get_film_info():
    title = request.args.get("film_title", "")
    if not title:
       return jsonify({"error": "film_title is required."}), 400

    try:
        search = requests.get(f"{TMDB_BASE}/search/movie",
                            params={"query": title, "api_key": API_KEY},
                            timeout=10)
        search.raise_for_status()
        results = search.json().get("results", [])
    except requests.exceptions.RequestException:
        return jsonify ({"error":"Couldn't reach TMDB"}), 502

    if not results:
        return jsonify({"error":"Couldn't get data."}), 404
      
    return jsonify(results[0]), 200


@app.route('/api/all/watched_film', methods =["POST"])
def add_watched_films():
    data = request.get_json()
    title = (data.get("title"))
    if not title:
        return jsonify({"error": "Film title is required"}), 400
    
    try:
        film = search_tmdb(title)

    except requests.exceptions.RequestException:
        return jsonify({"error": "Couldn't reach TMDB"}), 400
    
    if not film:
        return jsonify({"error": f"{title} not found in TMDB"}), 404

    official_title = film["title"]

    try:
        existing_titles = [row[0].lower() for row in dbutils.fetch_all_movies()]
        if official_title.lower() in existing_titles:
             return jsonify({"error": f"{official_title} is already in your library"}), 409

        sql_query.new_watched_film(
            official_title, 
            film["id"], 
            film.get("overview", None)
            )

    except mysql.connector.Error:
           return jsonify ({"error": "There seems to be an error with the database."}), 500
    
    return jsonify ({"title": official_title, "watched": True}), 200
    




# ===================================================================
#                         SUBSCRIPTIONS
# ===================================================================

if __name__ == "__main__":
    app.run(debug=True, port=5000)

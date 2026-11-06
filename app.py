from flask import Flask, jsonify, request       # re-added request - RB
from DButils import FilmDB, seedDB
from config import DB_manager
from TMDB_endpoints import TMDB
from tmdb_api import TMDB_api
from graph import Graph
from graph_build import GraphBuild
import os
import requests
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")


import mysql.connector

app = Flask(__name__)

dbutils = FilmDB("cinefiles")      # creates instance of FilmDB class, can be resused - RB
# sql_query = FilmDB(DB_manager())     # added now that add_physical_copy in class SQL_query - RB, removing post Olivia's DButils redo - RB

# ===================================================================
#                           SEE OVERVIEW
# ===================================================================

@app.route('/api/overview')
def get_overview():
    print("in overview")
    overview = FilmDB("cinefiles").fetch_overview()         # reuse dbutils variable above for consistency? - RB
    return jsonify({"data": overview}), 200

# ===================================================================
#                        SEE WATCHED FILMS
# ===================================================================

@app.route('/api/all')
def get_all_movies():
    cinefiles = FilmDB("cinefiles")                         # reuse dbutils variable above for consistency? - RB
    movies = cinefiles.fetch_all_movies() #see DButils.py
    return jsonify({"data": movies}), 200 #This is mock. ATM fetch_all_movies doesn't return anything useful

# ===================================================================
#                        GET RECOMMENDATION
# ===================================================================
@app.route("/get-recommendation", methods=["GET"])
def get_recommendation():
    api_key = TMDB_api(TMDB, API_KEY)
    db = FilmDB("cinefiles")
    graph = Graph()
    graph_builder =GraphBuild(graph,db)
    graph_builder.build()
    watched_movies = graph_builder.movie_titles()
    genres, people = graph_builder.dfs(graph_builder.start_node)
    recommendation = api_key.get_recommendation(genres, people, watched_movies)

    if recommendation is None:
        return jsonify({"error": "No recommendations found"}), 404

    return jsonify({"recommendations": recommendation})

# ===================================================================
#                          HOW TO WATCH
# ===================================================================

@app.route("/api/how-to-watch/<movie>")
def how_to_watch(movie):
    stream_info = TMDB_api(TMDB, API_KEY)
    stream = stream_info.find_movie_subscription(movie)
    if stream is None:

        return jsonify({"error": "Couldn't get film data"}), 404
    return jsonify(stream)

@app.route("/api/owned-physical/<movie>", methods=["GET"])
def physical_copy(movie):

    physical = FilmDB("cinefiles")
    result = physical.fetch_owned_copy(movie)

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

        dbutils.add_physical_copy(film, physical_format)        # Updated to use dbutils again - RB
        return {"message": "You've added a physical copy to your library"}, 200
    
    except mysql.connector.IntegrityError:
        return jsonify({"error": "There was a problem adding this format to your library."}), 409 # Conflict

    except ValueError:
        return jsonify({"error": "Invalid physical format"}), 400
    
    except mysql.connector.Error:
        return jsonify({"error": "There was a problem with the database"}), 500 # Internal Server Error

# ===================================================================
#                         ADD WATCHED FILM
# ===================================================================
TMDB_BASE = "https://api.themoviedb.org/3"

def search_tmdb(title):
    search = requests.get (f"{TMDB_BASE}/search/movie", params={"query": title, "api_key": API_KEY})

    search.raise_for_status()
    results = search.json().get("results", [])
    if not results:
        return None

    film_id = results[0]["id"]
    details = requests.get(f"{TMDB_BASE}/movie/{film_id}", params={"api_key": API_KEY, "append_to_response":"credits"})
    details.raise_for_status()
    details = details.json()

    credits = details.get("credits", {})
    return{
        "tmdb_id": details["id"],
        "title": details["title"],
        "overview": details.get("overview"),
        "genres": [g["name"] for g in details.get("genres", [])],
        "directors": [c["name"] for c in credits.get("crew", []) if c["job"] == "Director"],
        "actors": [c["name"] for c in credits.get("cast", [])[:3]],
    }

@app.route("/api/all/film_info")
def get_film_info():
    title = request.args.get("film_title", "")
    if not title:
       return jsonify({"error": "film_title is required."}), 400

    try:
        search = requests.get(f"{TMDB_BASE}/search/movie",
                            params={"query": title, "api_key": API_KEY})
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
        return jsonify({"error": f"Couldn't reach TMDB for {title}"}), 502
    
    if not film:
        return jsonify({"error": f"{title} not found in TMDB"}), 404

    official_title = film["title"] 

    try:
        existing_titles = [row[0].lower() for row in dbutils.fetch_all_movies()]
        if official_title.lower() in existing_titles:
            return jsonify({"error": f"{official_title} is already in your library"}), 409

    
        dbutils.new_watched_film(film)
    except mysql.connector.Error:
        return jsonify({"error": "There was a problem with the database"}), 500 
         
    return jsonify ({"title": official_title, "watched": True}), 200
    

@app.route('/api/init')
def new_user_init():
    # seedDB("cinefiles").dropDB()
    check = FilmDB('cinefiles').check_db_exists()
    if not check:
        init = seedDB('cinefiles')
        init.init_db()
        init.seed_subscriptions()
        return jsonify({"msg": "Auto setup complete"}),200
    else:
        return jsonify({"msg": "Initialised"}),200


# ===================================================================
#                         SUBSCRIPTIONS
# ===================================================================

if __name__ == "__main__":
    app.run(debug=True, port=5000)

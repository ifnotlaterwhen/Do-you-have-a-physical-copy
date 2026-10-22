from flask import Flask, jsonify
from DButils import FilmDB #import the class

app = Flask(__name__)

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



# ===================================================================
#                         ADD PHYSICAL COPY
# ===================================================================

@app.route('api/all/search')
def find_film_id():
    return jsonify({"message": "Temporary code: endpoint is working!"}), 200

@app.route('/api/all/<int:my_film_id', methods=['PATCH'])
def update_physical():
    return jsonify({"message": "Temporary code: endpoint is working!"}), 200

# ===================================================================
#                         ADD WATCHED FILM
# ===================================================================



# ===================================================================
#                         SUBSCRIPTIONS
# ===================================================================


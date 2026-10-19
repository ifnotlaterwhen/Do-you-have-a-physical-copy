from flask import Flask, jsonify
from DButils import FilmDB #import the class
from config import manager_instance #import the DB connector class instance to pass into FilmDB instance

app = Flask(__name__)


@app.route('/api/all')
def get_all_movies():
    cinefiles = FilmDB(manager_instance)
    movies = cinefiles.fetch_all_movies() #see DButils.py
    return jsonify({"data": movies}), 200 #This is mock. ATM fetch_all_movies doesn't return anything useful

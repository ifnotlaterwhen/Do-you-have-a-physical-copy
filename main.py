import requests
from pprint import pprint
def run():
    print("Welcome to Cinefiles")
    menu()

def menu():
    choice = int(input("""Please enter the number:
    1. Cinefiles DB
    1- Film recommandations 
    2- Find where to watch
    3- Add physical copy
    4- Add watched film
    5- Subscriptions
    """))


#Reese's note to all: 
# the functions below should call API routes defined in app.py
# the routes defined in app.py should call funcitons in DButils to actually query the DB
# Since we don't have the above defined yet, please write placeholder functions in both app.py and DButils.py
# See show_DB for example of placeholders

def show_DB():
    # Reese's note: I realised we don't have a fuction for users to get an overview of their movies
    # For now I will add show_DB, but we will discuss further what it does exactly
    # this function should query cinefiles DB and show info of all watched/want to watch/owned movies

    all_movies = requests.get("http://127.0.0.1:8888/api/all") #See app.py for this route
    pprint(all_movies.json())



#Leave it for now
def get_recommendatoins():
    # should return a number of movies based on watch history 
    pass

#Carina
def find_stream():
    # this should call the TMDB api
    # this should allow users to provide the film title
    # should we consider resuability, like when/if the users go to a specific movie info page, 
    # they should be able to call this function too?
    pass

#Reid
def log_physical(): 
    # Updates the physical copy column of the movie passed in as argument if it already exists in the DB
    # Add a new movie to DB with the physical copy column set to True
    pass

#Stéphanie
def add_films():
    # This allows users to add a film that they want to watch or have watched.
    # It should also allow them to say if they already have a physical copy when adding the film.
    # 2 potential ways to do this: 
    # Option 1: We collect user input in a dict (film name, watched, physical copy owned etc) 
    #   and add that to the DB via 1 single query
    # Option 2: Add the new film to the DB without stating physical copy in the query body (should default to False),
    #   then call log_physical() to handle it .
    # Reese's message to Stéphanie: Lmk your thoughts.
    pass

def adjust_subscription():
    # queries the DB to show a list of subscribed services

    # should have a  mini menu
    # 1. allows users to log a new subscribed film streaming service.
    # 2. remove a subscrfiption from the list.
    pass

if __name__ == "__main__":
    run()
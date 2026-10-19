import requests
from pprint import pprint

def run():
    print("Welcome to Cinefiles")
    while True:
        choice = menu()
        result = ""
        if choice == 1:
            result = show_DB()
        elif choice == 2:
            result = get_recommendatoins()
        elif choice == 3:
            result = find_stream()
        elif choice == 4:
            result = log_physical()
        elif choice == 5:
            result = add_films()
        elif choice == 6:
            result = view_subscription()
        elif choice == 7:
            break

        if result:
            if not return_to_menu():
                break
        else:
            print("Something went wrong. Please try again")


def menu():
    print("""1- Cinefiles DB
    2- Film recommandations 
    3- Find where to watch
    4- Add physical copy
    5- Add watched film
    6- Subscriptions
    7- exit""")

    choice = 1
    while True:
        try:
            choice = int(input("Please enter the number from the menu: "))
            if 1<= choice <= 7:
                break
        except ValueError:
            print("Please enter a valid number")
        else:
            print("Pease enter a number on the menu (1-7)")

def return_to_menu():
    another = input("Would you like to go back to the menu? y/n: ").lower()
    if another != "y" and another != "n":
        raise ValueError("Please enter y or n:")
    elif another == "n":
        return False
    else:
        return True
            


#Reese's note to all: 
# the functions below should call API routes defined in app.py
# the routes defined in app.py should call funcitons in DButils to actually query the DB
# Since we don't have the above defined yet, please write placeholder functions in both app.py and DButils.py
# See show_DB for example of placeholders

def show_DB():
    # Reese's note: I realised we don't have a fuction for users to get an overview of their movies
    # For now I will add show_DB, but we will discuss further what it does exactly
    # this function should query cinefiles DB and show info of all watched/owned movies

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
    # This allows users to add a film that they have watched.
    # It should also allow them to say if they already have a physical copy when adding the film.
    # 2 potential ways to do this: 
    # Option 1: We collect user input in a dict (film name, watched, physical copy owned etc) 
    #   and add that to the DB via 1 single query
    # Option 2: Add the new film to the DB without stating physical copy in the query body (should default to False),
    #   then call log_physical() to handle it .
    # Reese's message to Stéphanie: Lmk your thoughts.
    pass

def view_subscription():
    # queries the DB to show a list of subscribed services
    # press 1 to adjust subscriptions, 2 to go back to main menu (break)
    # calling adjust_subscription is optional
    pass

def adjust_subscription():
    # display a full list of avaliable subscriptions numbered (regardless of whether the user is subscribed to it)
    # select a number for the one you want to update
    # 1. allows users to add the subscription
    # 2. remove a subscrfiption from the list.
   pass

if __name__ == "__main__":
    run()
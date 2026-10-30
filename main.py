import requests
from pprint import pprint
from app import how_to_watch
from tabulate import tabulate

class ValueTooLow(Exception):
    pass
class ValueTooHigh(Exception):
    pass

base_url = "http://127.0.0.1:5000"
current_film = ""

def run():
    print("\nWelcome to Cinefiles")
    while True:
        choice = menu()
        result = ""
        if choice == 1:
            result = show_DB()
            # show_DB()
        elif choice == 2:
            result = get_recommendations()
            # get_recommendations()
        elif choice == 3:
            result = how_watch()
            # how_watch()
        elif choice == 4:
            result = log_physical()
            # log_physical()
        elif choice == 5:
            result = add_films()
            # add_films()
        elif choice == 6:
            result = view_subscription()
            # view_subscription()
        elif choice == 7:
            print("\nBye for now!\n")
            break

        if result:
            # if not return_to_menu():
                # break
            break
        # else:
        #     print("Something went wrong. Please try again")

def menu():
    print("""
[1] Cinefiles DB
[2] Film recommandations 
[3] Find where to watch
[4] Add physical copy
[5] Add watched film
[6] Subscriptions
[7] Exit\n""")

    # choice = 1
    while True:
        try:
            choice = int(input("Please enter the number from the menu: "))
            
            if choice < 1:
                raise ValueTooLow
            if choice > 7:
                raise ValueTooHigh

            return choice
        
        except ValueError:
            print("Please enter a valid number")
        # else:
        #     print("Pease enter a number on the menu (1-7)")
        except ValueTooLow:
            print("\nNumber too low. Pease enter a number on the menu (1-7)\n")
        except ValueTooHigh:
            print("\nNumber too high. Pease enter a number on the menu (1-7)\n")


# def return_to_menu():
#     another = input("\nWould you like to go back to the menu? y/n: ").lower()
#     if another != "y" and another != "n":
#         raise ValueError("Please enter y or n:")
#     elif another == "n":
#         return False
#     else:
#         return True

#Reese's note to all: 
# the functions below should call API routes defined in app.py
# the routes defined in app.py should call funcitons in DButils to actually query the DB
# Since we don't have the above defined yet, please write placeholder functions in both app.py and DButils.py
# See show_DB for example of placeholders

# ===================================================================
#                        SEE WATCHED FILMS
# ===================================================================

def show_DB():
    all_movies = requests.get(f"{base_url}/api/overview") #See app.py for this route
    table = tabulate(all_movies.json()["data"], headers=['Title', 'genre', 'directed by', 'starring','4k bluray', 'blyray', 'dvd'], tablefmt='markdown')
    # print(all_movies.json()["data"])
    print(table)
    return True

# ===================================================================
#                        GET RECOMMENDATION
# ===================================================================

#Leave it for now
def get_recommendations():
    # should return a number of movies based on watch history 
    pass

# ===================================================================
#                          HOW TO WATCH
# ===================================================================

#Carina
def how_watch():
    # this should call the TMDB api
    # this should allow users to provide the film title
    # should we consider resuability, like when/if the users go to a specific movie info page, 
    # they should be able to call this function too?
    # need to also note if any physical copy, and what format(s)

    movie_title = input("What movie whould you like to know where to stream?")
    if not movie_title:
        print("Please type the name of the movie")
        return None

    streaming = requests.get(f"http://127.0.0.1:5000/api/how-to-watch/{movie_title}")
    owned = requests.get(f"http://127.0.0.1:5000/api/owned-physical/{movie_title}")
    if owned.status_code == 200:
        owned_copy = owned.json()
    else:
        owned_copy = None

    if owned_copy:
        print(f"You have {movie_title} on {owned_copy}")
    else:
        print(f"you do not own {movie_title}. But...")

    return streaming.json()




# ===================================================================
#                         ADD PHYSICAL COPY
# ===================================================================

#Reid

# When the user enters a film, check if it exists. If not, film added to DB before the logic proceeds       # part of add_films?
# Updates the relevant value of dvd_owned/bluray_owned/4k_bluray_owned to True in DB

# below is on the basis that the film already exists in the database.

def physical_menu():
    print("""
[1] DVD
[2] Blu-ray 
[3] 4K Blu-ray
[4] Return to Main Menu
[5] Exit\n""")

    while True:
        try:
            choice = int(input("Please enter the number from the menu: ").strip())
            if choice < 1:
                raise ValueTooLow
            if choice > 5:
                raise ValueTooHigh
            return choice
        except ValueError:
            print("Please enter a valid number")
        except ValueTooLow:
            print("\nNumber too low. Pease enter a number on the menu (1-5)\n")
        except ValueTooHigh:
            print("\nNumber too high. Pease enter a number on the menu (1-5)\n")

def physical_options():
    print("\nWhich physical format do you want to add? ")
    choice = physical_menu()
    if choice == 1:
        return "dvd_owned"
    elif choice == 2:
        return "bluray_owned"
    elif choice == 3:
        return "4k_bluray_owned"
    elif choice == 4:
        print("\nGoing back to the Main Menu\n")
        return None
    elif choice == 5:
        return "exit"

def log_physical():
    
    # call whichever adding film function from Stéphanie, which should also update univeral current_film variable - RB

    physical_format = physical_options()

    if physical_format is None:
        return

    if physical_format == "exit":
        return True

    data = {
        "title" : current_film,
        "physical_format" : physical_format
    }

    try:
        url = (f"{base_url}/api/all/physical")
        response = requests.patch(url, json=data)
        if response.status_code == 200:
            print("\nYour physical copy has been stored in your library")
            return
        else:
            print(f'\nSorry there was an error: {response.json()["error"]}')
            return
    except requests.exceptions.RequestException:
        print("\nSorry, there was an issue. Make sure app.py is running and then run main.py again\n")
        return

    # # Find film ID:

    # url_search = (f"{base_url}/api/all/search")
    # response = requests.get(url_search, json=data)

    # if response.status_code == 200:
    #     film_search = response.json()
    #     my_film_id = film_search["my_film_id"]
    # else:
    #     print(f'\n** Error: {response.json()["error"]} **')
    #     return  # Need something for menu stuff here?

    # # Update physical format info:

    # url_id = (f"{base_url}/api/all/{my_film_id}")
    # response = requests.patch(url_id, json=data)

    # if response.status_code == 200:
    #     print("\nYour physical copy has been stored to your library")
    #     return  # Need something for menu stuff here?                          
    # else:
    #     print(f'\nSorry there was an error: {response.json()["error"]}')
    #     return  # Need something for menu stuff here?

    # # except requests.exceptions.RequestException: # Error for Flask communication not happening
    #     print("\nSorry, there was an issue. Make sure app.py is running and then run main.py again\n")
    #     return True
    #     # ask if go back to main menu or exit? or just exit for them??

# ===================================================================
#                         ADD WATCHED FILM
# ===================================================================

# Can I check your logic will handle the below please - RB
#   - Checks for an existing film before inserting. 
#   - Adds a new film to the DB if necessary (which gets the TMDB API to give you relevant metadata needed to populate the DB).
#   - Returns the film title to current_film global variable.

#Stéphanie
def add_films():
    global current_film     # just adding this so that the current_film variable up the top of the file acts properly as a global one - RB
    
    current_film = input("What's the film title you want to add to the library?").lower() # do we want to make this lower? shouldn't we retain capitalisation for when titles get returned to the user? - RB

    film_title = add_film_to_library(watched = True)

    if film_title is None:
        print("\nGoing back to the Main Menu\n")
        return None
    
    print(f"\n'{film_title}' has been added to your watched films.")
        
    # owns_copy = input("Do you own a physical copy of the film?\n y/n? ").lower()      # can we remove the call for Add Physical logic from your function? makes the logic a bit more funky for me using yours to check a title is on the DB. They can just add a physical copy easily from the main menu as needed - RB
    # if owns_copy == 'y':
    #    log_physical()

    # elif owns_copy == "n":
    #     print("No worries, your film has been saved without a physical copy.")
    
    # else:
    #     print("Please enter y or n")

def add_film_to_library(watched= True):
    global current_film 

    # does this need a check to see if the title is already on the DB, or is that handled elsewhere? - RB

    film_title = input("Please enter the name of the film:")        # remove? already asked in add_films. Let me know which way round you have the title and other logic from, and I'll call that one from my Add Physical stuff - RB
    if not film_title:
        print("Please enter a valid title.")
    
          
    film_data = {"title": film_title, "watched": watched}
    
    try:
        response = requests.post(f"{base_url}/api/all", json= film_data)
    
    except requests.exceptions.RequestException:
        print("Sorry there was an issue with your post request.")

    if response.status_code not in (200, 201):
        print(f"Sorry there seemed to have been an error {response.json()['error']}")
    current_film = film_title 
    return film_title                        

 
# ===================================================================
#                         SUBSCRIPTIONS
# ===================================================================

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
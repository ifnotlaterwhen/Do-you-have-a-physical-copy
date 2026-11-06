import requests
from pprint import pprint
from app import how_to_watch
from app import get_recommendation
from tabulate import tabulate

class ValueTooLow(Exception):
    pass
class ValueTooHigh(Exception):
    pass

base_url = "http://127.0.0.1:5000"
current_film = ""

def run():
    print("\nWelcome to Cinefiles")
    # The new function DB_init is for initialising the DB for the USER. 
    # It checks if cinefiles DB exists. 
    # If it doesn't, it will create a fresh DB with no seeding data except a list of subscriptions default to inactive.

    DB_init()

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
[2] Film recommendations 
[3] Find where to watch
[4] Add physical copy
[5] Track a film
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
            print("\nPlease enter a valid number\n")
        # else:
        #     print("Pease enter a number on the menu (1-7)")
        except ValueTooLow:
            print("\nNumber too low. Pease enter a number on the menu (1-7)\n")
        except ValueTooHigh:
            print("\nNumber too high. Pease enter a number on the menu (1-7)\n")


def return_to_menu():
    choice = input("\nBack to the main menu? (y/n): ").lower()
    if choice != "y" and choice != "n":
        raise ValueError("Please enter y or n:")
    elif choice == "n":
        return True

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
    table = tabulate(all_movies.json()["data"], headers=['Title', 'genre', 'directed by', 'starring','4k blu-ray', 'blu-ray', 'dvd'], tablefmt='markdown')
    # print(all_movies.json()["data"])
    print(table)
    return return_to_menu()

# ===================================================================
#                        GET RECOMMENDATION
# ===================================================================


def get_recommendations():
    # should print a number of movies based on watch history
    try:
        response= requests.get(f"http://127.0.0.1:5000/get-recommendation")
    except requests.RequestException:
        print("sorry, there seems to be a problem")
        return None
    if response.status_code != 200:
        print("sorry, could not find any recommendations")
        return None
    recommendations = response.json()["recommendations"]
    print("Here are some recommendations based on your viewing preference")
    print(recommendations)

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

    movie_title = input("What movie whould you like to know where to stream? ")
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

    data = streaming.json()
    print(data)



# ===================================================================
#                         ADD PHYSICAL COPY
# ===================================================================

#Reid

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
            print("\nPlease enter a valid number\n")
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
    
    global current_film

    add_films(return_message = False)
    if not current_film:
        return None

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

# ===================================================================
#                         ADD WATCHED FILM
# ===================================================================
def add_films(return_message=True):
    global current_film

    title = input("\nWhat film would you like to add to the library? ")
    if not title:
        print("Please enter a film title.")
        return None

    added_title = add_film_to_library(title, watched=True)

    if added_title is None:
        if return_message:
            print("\nGoing back to the Main Menu\n")
        return None

    current_film = added_title
    print(f"\n'{current_film}' has been added to your tracked films.")


def add_film_to_library(film_title, watched=True):

    film_data = {"title": film_title, "watched": watched}

    try:
        response = requests.post(f"{base_url}/api/all/watched_film", json=film_data)

    except requests.exceptions.RequestException:
        print("Sorry, there was an issue with your post request.")
        return None

    if response.status_code not in (200, 201):
            try:
                message = response.json().get("error", "Unknown error")
            except ValueError:
                print(f"Sorry, there seems to be an error:(Status{response.status_code}): {response.text}")
            return None

    return response.json().get("title", film_title)

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

def DB_init():
    check = requests.get(f"{base_url}/api/init").json()
    print(check["msg"])

if __name__ == "__main__":
    run()
    #how_watch()    # don't think should be called here, messes up the user flow

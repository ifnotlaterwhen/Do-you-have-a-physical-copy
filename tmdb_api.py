import requests
from dotenv import load_dotenv
from TMDB_endpoints import genres_ids, persons_ids, discover,search_movie
load_dotenv()

class TMDB_api:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.__api_key = api_key
        self.genre_id_cache = {}

# method that calls the external api, and check for connection success
    def api_request(self, api_endpoint, query_params=None):
            url = f"{self.api_url}{api_endpoint}"

            params = {"api_key": self.__api_key}
            if query_params:
                params.update(query_params)

            try:
                response = requests.get(url, params=params)
            except requests.RequestException:
                print("Unable to find api")
                return None

            if response.status_code != 200:
                print("Unable to retrieve data from api")
                return None

            return response.json()


# method to get the movie id
    def get_movie_id(self, movie) :
        params = {"query": movie}
        data = self.api_request(search_movie, params)
        if data is None:
            return None

        results = data["results"]
        if not results:
            return None

        return results[0]["id"]



#method to find where to stream movies in the UK
    def find_movie_subscription(self, movie):
        movie_id = self.get_movie_id(movie)
        if movie_id is None:
            return None

        data = self.api_request(f"/movie/{movie_id}/watch/providers")
        if data is None:
            return None

        # filter the results by UK only
        uk = data["results"].get("GB", {})

        # filter the results further by getting the flatrate key in the api json result, to get the streaming site info
        streaming_services = uk.get("flatrate")
        if not streaming_services:
            return f"{movie} is not streaming on any UK subscription service"

        returned_data = streaming_services[0]["provider_name"]
        return f"you can stream {movie} on {returned_data}"

    # retrieve the genre id and person id to find movie recommendation
    def genre_id(self, genre):
        if not self.genre_id_cache:
            endpoint = self.api_request(genres_ids)
            if endpoint is None:
                return None
            results = endpoint["genres"]


            for items in results:
                self.genre_id_cache[items["name"]] = items["id"] #<- store genres in a dictionary to avoid having to call the api everytime. then use the ids in the dict to fewtch genre id

        genre_results = []
        for genres in genre:
            name = genres.replace("Genre:", "")

            if name in self.genre_id_cache:
                    genre_results.append(str(self.genre_id_cache[name]))

        return "|".join(genre_results)


    def person_id(self, person):
    # split person id into 2 groups actor, director for recommendation parameters
        cast_id = []
        crew_id = []

        for node in person:
           role, name = node.split(":",1)
           people = self.api_request(persons_ids, {"query": name})
           if people is None:
               return None, None

           results = people["results"]

           if not results:
             continue

           if role == "Actor":
                cast_id.append(str(results[0]["id"]))
           elif role == "Director":
                crew_id.append(str(results[0]["id"]))

        return "|".join(cast_id), "|".join(crew_id) #<- oring the results so that the api will either choose one or the other in recommendation paramaeters


# recommendation logic
    def get_recommendation(self, genre, person, watched_titles):
        params = {
            "page": 1,
            "region": "GB",
            "sort_by": "popularity.desc",
}
        genre_ids = self.genre_id(genre)
        cast_ids, crew_ids = self.person_id(person)

        if genre_ids:
            params["with_genres"] = genre_ids
        if cast_ids:
            params["with_cast"] = cast_ids
        if crew_ids:
            params["with_crew"] = crew_ids

        recommend = self.api_request(discover, params)
        if recommend is None:
            return None
        results = recommend["results"]
 # check if results of the api movies matched movies nodes
        titles = []
        for movie in results:
            if movie["title"] not in watched_titles:
                titles.append(movie["title"])
                if len(titles) == 3: #<- only return at most 3 results
                    break

        if not titles:
            return None

        return ", ".join(titles)


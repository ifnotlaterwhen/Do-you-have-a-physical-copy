import requests
from dotenv import load_dotenv
load_dotenv()

class TMDB_api:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.__api_key = api_key

# method that calls the external api, and check for connection success
    def api_request(self, api_endpoint, query_params=None):
            url = f"{self.api_url}{api_endpoint}"

            params = {"api_key": self.__api_key}
            if query_params:
                params.update(query_params)

            try:
                response = requests.get(url, params=params, timeout=10)
            except requests.RequestException:
                print("Unable to find api")
                return None

            if response.status_code != 200:
                print("Unable to retrieve data from api")
                return None

            return response.json()


# method to get the movie id
    def get_movie_id(self, movie:str) -> int | None:
        params = {"query": movie}
        data = self.api_request("/search/movie", params)
        results = data["results"]
        if not results:
            return None

        return results[0]["id"]



#method to find where to stream movies in the UK
    def find_movie_subscription(self, movie:str) ->str | None:
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


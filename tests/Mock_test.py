import pytest
import requests
from tmdb_api import TMDB_api

baseUrl = "https://api.themoviedb.org/3"

class Test_TMDBapi:
    def test_response_success(self, mocker):
        response = TMDB_api(baseUrl, "fake-api-key")
        mock_response = mocker.Mock(status_code=200)
        mock_response.json.return_value = {"results": []}
        mocker.patch("tmdb_api.requests.get", return_value=mock_response)
        assert response.api_request("/search/movie") == {"results":[]}

    def test_response_failure(self, mocker):
        response = TMDB_api(baseUrl, "fake-api-key")
        mocker.patch("tmdb_api.requests.get", return_value=mocker.Mock(status_code=404))
        assert response.api_request("/search/movie") is None

    def test_movie_id(self, mocker):
        mock_data = {
            "results": [
                {
                    "adult": False,
                    "id": 550,
                    "original_language": "en",
                    "original_title": "Fight Club",
                }
            ]
        }
        mock_response = mocker.MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_data
        mocker.patch("tmdb_api.requests.get", return_value=mock_response)

        response = TMDB_api(baseUrl, "fake-api-key")
        response.get_movie_id("Fight Club")
        assert response.get_movie_id("fight club") == 550




    def test_movie_subscription(self, mocker):
        data = {
            "id": 550,
            "results": {
                "GB": {
                    "flatrate": [
                        {
                            "provider_id": 2,
                            "provider_name": "Disney Plus",
                            "display_priority": 1,
                        }
                    ]
                },
            },
        }


        search_id = mocker.MagicMock(status_code=200)

        search_id.json.return_value = {"results": [{"id": 550}]}

        streaming_provider =  mocker.MagicMock(status_code= 200)
        streaming_provider.json.return_value = data

        mocker.patch("tmdb_api.requests.get", side_effect=[search_id, streaming_provider] )
        mock_response = TMDB_api(baseUrl, "fake-api-key")
        result = mock_response.find_movie_subscription("fight club")


        assert result == "you can stream fight club on Disney Plus"



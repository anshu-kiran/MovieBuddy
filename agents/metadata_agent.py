from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import requests
import os
from dotenv import load_dotenv

load_dotenv()
OMDB_API_TOKEN = os.getenv("OMDB_API_TOKEN")
TMDB_API_TOKEN = os.getenv("TMDB_API_TOKEN")

class MetadataAgent:
    def __init__(self):
        self.omdb_api_key = OMDB_API_TOKEN
        self.tmdb_api_key = TMDB_API_TOKEN

    def fetch_metadata(self, state):
        """Fetch metadata from OMDB and TMDB."""
        title = state["input"]

        omdb_url = f"http://www.omdbapi.com/?t={title}&apikey={self.omdb_api_key}"
        omdb_response = requests.get(omdb_url)
        omdb_data = omdb_response.json()

        if omdb_response.status_code != 200 or omdb_data.get("Response") != "True":
            return {"error": f"Could not fetch metadata for '{title}' from OMDB."}

        imdb_id = omdb_data.get("imdbID")

        tmdb_id = None
        if imdb_id:
            tmdb_url = f"https://api.themoviedb.org/3/find/{imdb_id}"
            tmdb_params = {"api_key": self.tmdb_api_key, "external_source": "imdb_id"}
            tmdb_response = requests.get(tmdb_url, params=tmdb_params)
            tmdb_data = tmdb_response.json()

            if tmdb_response.status_code == 200 and "movie_results" in tmdb_data and tmdb_data["movie_results"]:
                tmdb_id = tmdb_data["movie_results"][0]["id"]

        if not tmdb_id:
            tmdb_url = "https://api.themoviedb.org/3/search/movie"
            tmdb_params = {"query": title, "api_key": self.tmdb_api_key}
            tmdb_response = requests.get(tmdb_url, params=tmdb_params)
            tmdb_data = tmdb_response.json()

            if tmdb_response.status_code == 200 and "results" in tmdb_data and tmdb_data["results"]:
                tmdb_id = tmdb_data["results"][0]["id"]

        omdb_data["tmdb_id"] = tmdb_id or "N/A"  # Default to "N/A" if TMDB ID is not found
        return {"metadata": omdb_data}
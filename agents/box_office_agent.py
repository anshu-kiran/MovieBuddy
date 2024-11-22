import requests
import logging
import os
from dotenv import load_dotenv

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_TOKEN")

class BoxOfficeAgent:
    def __init__(self):
        self.omdb_api_key = OMDB_API_KEY
        logging.basicConfig(level=logging.INFO)

    def fetch_box_office(self, state):
        """Fetch box office data for a movie using OMDB API."""
        metadata = state.get("metadata")
        if not metadata:
            return {"box_office": "No metadata available to fetch box office data."}

        title = metadata.get("Title")
        if not title:
            return {"box_office": "No title found in metadata."}

        try:
            url = f"http://www.omdbapi.com/?t={title}&apikey={self.omdb_api_key}"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200 and data.get("Response") == "True":
                box_office = data.get("BoxOffice", "Box office data not available.")
                return {"box_office": box_office}
            else:
                logging.warning(f"Failed to fetch box office data: {data.get('Error', 'Unknown error')}")
                return {"box_office": "Box office data not available."}
        except Exception as e:
            logging.error(f"Error fetching box office data: {e}")
            return {"box_office": "Box office data not available."}

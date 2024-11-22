from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class LLMAgent:
    def __init__(self):
        self.llm = ChatOpenAI()

    def recommend_movies(self, state):
        metadata = state.get("metadata", {})
        preferences = state.get("preferences", {})
        
        prompt = PromptTemplate.from_template("""
        You are a movie recommendation assistant. Based on the following information:

        Metadata:
        Title: {Title}
        Genre: {Genre}
        IMDb Rating: {imdbRating}
        Year: {Year}

        Preferences:
        Genre: {preferred_genre}

        Recommend a movie title and justify your recommendation.

        Response format:
        Movie Title: <movie name>
        """)

        inputs = {
            "Title": metadata.get("Title", "N/A"),
            "Genre": metadata.get("Genre", "N/A"),
            "imdbRating": metadata.get("imdbRating", "N/A"),
            "Year": metadata.get("Year", "N/A"),
            "preferred_genre": preferences.get("genre", "N/A"),
        }

        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(inputs)
        movie_title = self.extract_movie_title(response)
        return {"output": f"{response}", "recommended_movie": f"{movie_title}"}

    def extract_movie_title(self, response: str) -> str:
        for line in response.splitlines():
            if "Movie Title:" in line:
                return line.split(":")[1].strip()
        return "No recommendation available"

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from transformers import pipeline
import requests
import os
from dotenv import load_dotenv

load_dotenv()
TMDB_API_TOKEN = os.getenv("TMDB_API_TOKEN")
DEFAULT_SENTIMENT = {
            "sentiment": {
                "overall": "N/A",
                "positive_reviews": 0,
                "negative_reviews": 0,
                "neutral_reviews": 0,
                "total_reviews": 0,
                "message": "No data available for sentiment analysis."
            }
        }

class SentimentAnalysisAgent:
    def __init__(self):
        self.tmdb_api_key = TMDB_API_TOKEN
        self.sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english", device=0, truncation=True)
        self.max_length = 512

    def fetch_reviews(self, tmdb_id):
        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/reviews"
        params = {"api_key": self.tmdb_api_key}
        response = requests.get(url, params=params)
        data = response.json()
        
        if response.status_code == 200 and "results" in data:
            reviews = [review["content"][:self.max_length] for review in data["results"]]
            return reviews
        else:
            return []

    def analyze_sentiment(self, state):
        metadata = state.get("metadata")
        if not metadata:
            return DEFAULT_SENTIMENT

        tmdb_id = metadata.get("tmdb_id")
        if not tmdb_id or tmdb_id == "N/A":
            return DEFAULT_SENTIMENT

        reviews = self.fetch_reviews(tmdb_id)
        if not reviews:
            return DEFAULT_SENTIMENT

        sentiments = self.sentiment_analyzer(reviews)

        positive_count = sum(1 for sentiment in sentiments if sentiment["label"] == "POSITIVE")
        negative_count = sum(1 for sentiment in sentiments if sentiment["label"] == "NEGATIVE")
        neutral_count = len(reviews) - positive_count - negative_count

        overall_sentiment = "positive" if positive_count > negative_count else "negative" if negative_count > positive_count else "neutral"

        return {
            "sentiment": {
                "overall": overall_sentiment,
                "positive_reviews": positive_count,
                "negative_reviews": negative_count,
                "neutral_reviews": neutral_count,
                "total_reviews": len(reviews),
                "message": "Sentiment analysis completed successfully."
            }
        }

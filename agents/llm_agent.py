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
        sentiment = state.get("sentiment", {
            "overall": "N/A",
            "positive_reviews": 0,
            "negative_reviews": 0,
            "neutral_reviews": 0,
            "total_reviews": 0,
            "message": "No sentiment analysis available."
        })

        prompt = PromptTemplate.from_template("""
            You are a movie recommendation assistant. Based on the following information:

            Metadata:
            Title: {Title}
            Genre: {Genre}
            IMDb Rating: {imdbRating}
            Year: {Year}

            Sentiment Analysis:
            Overall Sentiment: {overall}
            Positive Reviews: {positive_reviews}
            Negative Reviews: {negative_reviews}
            Neutral Reviews: {neutral_reviews}
            Total Reviews: {total_reviews}

            Additional Notes: {message}

            Recommend a movie based on this information and justify your recommendation.
        """)

        inputs = {
            "Title": metadata.get("Title", "N/A"),
            "Genre": metadata.get("Genre", "N/A"),
            "imdbRating": metadata.get("imdbRating", "N/A"),
            "Year": metadata.get("Year", "N/A"),
            "overall": sentiment["overall"],
            "positive_reviews": sentiment["positive_reviews"],
            "negative_reviews": sentiment["negative_reviews"],
            "neutral_reviews": sentiment["neutral_reviews"],
            "total_reviews": sentiment["total_reviews"],
            "message": sentiment["message"],
        }

        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(inputs)
        return {"output": response}

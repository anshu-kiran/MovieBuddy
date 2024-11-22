import os
from agents import SentimentAnalysisAgent  

def test_sentiment_analysis():
    state = {
        "metadata": {"tmdb_id": "550"}  
    }

    agent = SentimentAnalysisAgent()

    result = agent.analyze_sentiment(state)

    print("\n--- Sentiment Analysis Results ---")
    print(f"Overall Sentiment: {result['sentiment']['overall']}")
    print(f"Positive Reviews: {result['sentiment']['positive_reviews']}")
    print(f"Negative Reviews: {result['sentiment']['negative_reviews']}")
    print(f"Neutral Reviews: {result['sentiment']['neutral_reviews']}")
    print(f"Total Reviews: {result['sentiment']['total_reviews']}")
    print(f"Message: {result['sentiment']['message']}")

if __name__ == "__main__":
    test_sentiment_analysis()

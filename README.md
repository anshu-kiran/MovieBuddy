# MovieBuddy 🎥

This is a movie recommendation system that uses multiple agents to analyze and recommend movies based on sentiment, metadata, and user queries. It processes queries to find relevant movies, analyze their descriptions and metadata, and compute unified scores for ranking.

--------
### Tools and Models Used

- **Frameworks**: 
    - Streamlit (for UI)
    - LangChain and LangGraph (for agent orchestration)
- **APIs**: 
    - TMDB API (for metadata and posters)
    - OMDb API (for movie rankings such as IMDb ratings)
- **Models Used**:
    - gpt-3.5-turbo
    - distilbert/distilbert-base-uncased-finetuned-sst-2-english (for sentiment analysis)

## Installation
1. Clone the repository:

    ```git clone https://github.com/anshu-kiran/MovieBuddy.git```

2. Navigate to the project directory:

    ```cd MovieBuddy```

3. Install dependencies:

    ```pip install -r requirements.txt```

4. Copy the `.env_sample` to `.env` and add your own API keys.

5. Run the Streamlit app:

     ```streamlit run ui/streamlit_app.py```

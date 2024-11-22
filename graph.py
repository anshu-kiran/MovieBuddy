from langgraph.graph import StateGraph, END
from typing import Annotated, TypedDict
from agents import MetadataAgent, LLMAgent, SentimentAnalysisAgent, BoxOfficeAgent

class MovieState(TypedDict):
    input: str               # Movie title
    preferences: dict        # User preferences (e.g., genre)
    metadata: dict           # Metadata fetched from OMDB
    sentiment: dict          # Sentiment data
    box_office: str          # Box office details
    output: str              # Final output/recommendation

def create_graph():
    workflow = StateGraph(MovieState)

    metadata_agent = MetadataAgent()
    sentiment_agent = SentimentAnalysisAgent()
    box_office_agent = BoxOfficeAgent()
    llm_agent = LLMAgent()

    workflow.add_node("fetch_metadata", lambda state: metadata_agent.fetch_metadata(state))
    workflow.add_node("analyze_sentiment", lambda state: sentiment_agent.analyze_sentiment(state))
    workflow.add_node("llm_recommendation", lambda state: llm_agent.recommend_movies(state))
    workflow.add_node("fetch_box_office", lambda state: box_office_agent.fetch_box_office(state))

    workflow.set_entry_point("fetch_metadata")
    workflow.add_edge("fetch_metadata", "analyze_sentiment")
    workflow.add_edge("analyze_sentiment", "fetch_box_office")
    workflow.add_edge("fetch_box_office", "llm_recommendation")
    workflow.add_edge("llm_recommendation", END)

    return workflow.compile()

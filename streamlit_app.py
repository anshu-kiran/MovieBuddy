import os
import streamlit as st
from dotenv import load_dotenv
from graph import create_graph
import matplotlib.pyplot as plt

graph = create_graph()

st.title("MovieAgent 🎥")
st.write("Enter the title of a movie you love and your preferred genre to get recommendations from your very own MovieAgent!")

with st.form("movie_input_form"):
    movie_title = st.text_input("Movie Title", placeholder="e.g., Inception")
    genre_preference = st.text_input("Preferred Genre", placeholder="e.g., Action")
    submitted = st.form_submit_button("Get Recommendation")

if submitted:
    if not movie_title.strip():
        st.error("Please enter a movie title.")
    else:
        initial_state = {
            "input": movie_title.strip(),
            "preferences": {"genre": genre_preference.strip()},
        }

        with st.spinner("Fetching recommendations..."):
            result = graph.invoke(initial_state)

        st.subheader("Recommendation")
        st.write(result["output"])

        box_office_data = result.get("box_office", "Box office data not available.")
        st.subheader("Box Office Data")
        st.write(box_office_data)

        sentiment_data = result.get("sentiment", {
            "overall": "N/A",
            "positive_reviews": 0,
            "negative_reviews": 0,
            "neutral_reviews": 0,
            "total_reviews": 0
        })

        st.subheader("Sentiment Analysis")

        if sentiment_data["total_reviews"] > 0:
            labels = ["Positive", "Negative", "Neutral"]
            counts = [
                sentiment_data["positive_reviews"],
                sentiment_data["negative_reviews"],
                sentiment_data["neutral_reviews"]
            ]

            fig, ax = plt.subplots()
            ax.bar(labels, counts, color=["#AEC6CF", "#77DD77", "#CBAACB"])
            ax.set_title("Sentiment Distribution", fontsize=12)
            ax.set_ylabel("Number of Reviews", fontsize=10)
            plt.style.use('seaborn-v0_8-pastel')
            plt.grid(False)
            st.pyplot(fig)            

            st.write(f"**Overall Sentiment**: {sentiment_data['overall'].capitalize()}")
        else:
            st.info(f"No sentiment data available for **{recommended_movie}**.")

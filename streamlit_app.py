import os
import streamlit as st
from dotenv import load_dotenv
from graph import create_graph

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

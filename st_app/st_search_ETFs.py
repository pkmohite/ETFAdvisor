# file: st_app/st_search_ETFs.py
import streamlit as st
import json
import numpy as np
import pandas as pd
from st_recommender import ETFRecommender

st.header("ETF Recommender")

# Create an instance of ETFRecommender
recommender = ETFRecommender()

# Create a container for the input and reset button
input_container = st.container()

# Create two columns within the input container
col1, col2 = input_container.columns([6, 1])

# Get user input for investment strategy in the first column
user_input = col1.chat_input("Enter a description of the investment strategy:")

# Add reset button in the second column
if col2.button("Reset"):
    st.session_state.user_input = ""

if user_input:
    # Display user input in chat
    with st.chat_message("user"):
        st.write(user_input)

    # Get ETF recommendations
    recommendations = recommender.recommend_etfs(user_input)

    # Move to a pandas dataframe
    recommendations = pd.DataFrame(recommendations)

    # Remove embeddings, similarity score and ticker columns from the recommendations
    recommendations = recommendations.drop(
        columns=["embedding", "similarity", "ticker"]
    )

    # Display the recommendations in a st.dataframe
    st.dataframe(recommendations)

import streamlit as st
import json
import os
import numpy as np
from vertexai.language_models import TextEmbeddingModel

class ETFRecommender:
    def __init__(self):
        # Set the path to your service account key file
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_key.json"
        self.data = None

    def load_data(self, file_path):
        # Load the JSON data with embeddings from file
        with open(file_path, 'r') as file:
            self.data = json.load(file)

    def get_embedding(self, text):
        model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
        embeddings = model.get_embeddings([text])
        return embeddings[0].values

    def cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def recommend_etfs(self, user_input):
        # Generate embedding for user input
        user_input_embedding = self.get_embedding(user_input)

        # Calculate cosine similarity between user input and each ETF
        for etf in self.data:
            etf['similarity'] = self.cosine_similarity(user_input_embedding, etf['embedding'])

        # Sort ETFs based on similarity score
        self.data.sort(key=lambda x: x['similarity'], reverse=True)

        # Return top 5 ETF recommendations
        return self.data[:5]

    def run_app(self):
        st.header("ETF Recommender")

        # Load ETF data
        self.load_data('etf_data_short.json')

        # Create a container for the input and reset button
        input_container = st.container()
        
        # Create two columns within the input container
        col1, col2 = input_container.columns([6, 1])

        # Get user input for investment strategy in the first column
        user_input = col1.chat_input("Enter a description of the investment strategy:")

        # Add reset button in the second column
        if col2.button('Reset'):
            st.session_state.user_input = ""

        if user_input:
            # Display user input in chat
            with st.chat_message('user'):
                st.write(user_input)

            # Get ETF recommendations
            recommendations = self.recommend_etfs(user_input)

            # Remove embeddings, similarity score and ticker columns from the recommendations
            for recommendation in recommendations:
                recommendation.pop('embedding', None)
                recommendation.pop('similarity', None)
                recommendation.pop('ticker', None)        

            # Create a table for the recommendations
            recommendation_table = st.table(recommendations)


# Run the ETF Recommender app
etf_recommender = ETFRecommender()
etf_recommender.run_app()
import streamlit as st
import json
import os
import numpy as np
import thepassiveinvestor as pi
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

def etf_recommender_page():
    st.header("ETF Recommender")

    # Create an instance of ETFRecommender
    recommender = ETFRecommender()
    recommender.load_data('etf_data_short.json')

    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Add reset button
    if st.button('Reset Chat'):
        st.session_state.chat_history = []

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message['role']):
            st.write(message['content'])

    # Get user input for investment strategy
    user_input = st.chat_input("Enter a description of the investment strategy:")

    if user_input:
        # Add user input to chat history
        st.session_state.chat_history.append({'role': 'user', 'content': user_input})

        # Get ETF recommendations
        recommendations = recommender.recommend_etfs(user_input)

        # Create recommendation message
        recommendation_message = "Top 5 ETF Recommendations:\n"
        for i, etf in enumerate(recommendations):
            recommendation_message += f"{i+1}. {etf['long_name']} ({etf['ticker']})\n"
            recommendation_message += f"   {etf['summary']}\n"
            recommendation_message += f"   Similarity Score: {etf['similarity']}\n"

        # Display the recommendations in the chat
        with st.chat_message('assistant'):
            st.write(recommendation_message)

        # Add recommendations to chat history
        st.session_state.chat_history.append({'role': 'assistant', 'content': recommendation_message})
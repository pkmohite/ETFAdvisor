import json
import os
import requests
import numpy as np
import thepassiveinvestor as pi
from vertexai.language_models import TextEmbeddingModel

# Set the path to your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_key.json"

def get_embedding(text):
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    embeddings = model.get_embeddings([text])
    return embeddings[0].values

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Load the JSON data with embeddings from file
with open('etf_data_with_embeddings.json', 'r') as file:
    data = json.load(file)

while True:
    # Get user input for investment strategy
    user_input = input("Enter a description of the investment strategy (or type 'exit' to quit): ")
    
    if user_input.lower() == 'exit':
        print("Thank you for using the ETF Recommendation Tool!")
        break

    # Generate embedding for user input
    user_input_embedding = get_embedding(user_input)

    # Calculate cosine similarity between user input and each ETF
    for etf in data:
        etf['similarity'] = cosine_similarity(user_input_embedding, etf['summary_embedding'])

    # Sort ETFs based on similarity score
    data.sort(key=lambda x: x['similarity'], reverse=True)

    # Print top 5 ETF recommendations
    print("Top 5 ETF Recommendations:")
    for i in range(5):
        print(f"{i+1}. {data[i]['long_name']} ({data[i]['ticker']})")
        print(f"   {data[i]['summary']}")
        print(f"   Similarity Score: {data[i]['similarity']}")

    user_input = input("Do you want to compare the top 5 ETFs? (y/n): ")
    if user_input.lower() == "y":
        # Collect data from the top 5 ETFs and compare them
        etf_comparison = pi.collect_data([data[0]['ticker'], data[1]['ticker'], data[2]['ticker'], data[3]['ticker'], data[4]['ticker']], comparison=True)
        # Show the comparison
        print(etf_comparison)

    user_input = input("Do you want to download the analysis report? (y/n): ")
    if user_input.lower() == "y":
        # Download Analysis
        etf_report = [data[0]['ticker'], data[1]['ticker'], data[2]['ticker'], data[3]['ticker'], data[4]['ticker']]
        pi.create_ETF_report(etf_report, 'ETF Report.xlsx')
    else:
        print("No report downloaded.")
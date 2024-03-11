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

# Get user input
user_input = input("Enter a description of the investment strategy: ")

# Generate embedding for user input
user_input_embedding = get_embedding(user_input)

# Calculate cosine similarity between user input and each ETF
for etf in data:
    etf['similarity'] = cosine_similarity(user_input_embedding, etf['summary_embedding'])

# Sort ETFs based on similarity score
data.sort(key=lambda x: x['similarity'], reverse=True)

# Print top 3 ETF recommendations
print("Top 3 ETF Recommendations:")
for i in range(3):
    print(f"{i+1}. {data[i]['long_name']} {data[i]['ticker']}")
    print(f"   {data[i]['summary']}")
    print(f"   Similarity Score: {data[i]['similarity']}")


user_input = input("Do you want Comparison?: y/n ")
if user_input == "y":
    # Collect data from a set of ETFs and compare them
    etf_comparison = pi.collect_data([data[1]['ticker'], data[2]['ticker'], data[3]['ticker']], comparison=True)
    # Show the comparison
    print(etf_comparison)
user_input = input("Do you want to download analysis report?: y/n ")
if user_input == "y":
    # Download Analysis
    etf_report = [data[1]['ticker'], data[2]['ticker'], data[3]['ticker']]
    pi.create_ETF_report(etf_report, 'ETF Report.xlsx')
else:
    print("Thank You")
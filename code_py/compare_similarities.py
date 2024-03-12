import json
import os
import numpy as np
from scipy.spatial.distance import cosine, euclidean, cdist
from pyemd import emd
from vertexai.language_models import TextEmbeddingModel

# Set the path to your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_key.json"

def get_embedding(text):
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    embeddings = model.get_embeddings([text])
    return embeddings[0].values

def cosine_similarity(a, b):
    return 1 - cosine(a, b)

def euclidean_distance(a, b):
    return euclidean(a, b)

# def earth_movers_distance(a, b):
#     a = np.array(a)
#     b = np.array(b)
#     distance_matrix = cdist(a.reshape(-1, 1), b.reshape(-1, 1), metric='euclidean')
#     return emd(a, b, distance_matrix)

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

    # Calculate similarity scores using different methods
    cosine_scores = []
    euclidean_scores = []
    # emd_scores = []

    for etf in data:
        etf_embedding = etf['summary_embedding']
        cosine_scores.append(cosine_similarity(user_input_embedding, etf_embedding))
        euclidean_scores.append(euclidean_distance(user_input_embedding, etf_embedding))
        # emd_scores.append(earth_movers_distance(user_input_embedding, etf_embedding))

    # Sort ETFs based on similarity scores for each method
    cosine_top5 = sorted(zip(data, cosine_scores), key=lambda x: x[1], reverse=True)[:5]
    euclidean_top5 = sorted(zip(data, euclidean_scores), key=lambda x: x[1])[:5]
    # emd_top5 = sorted(zip(data, emd_scores), key=lambda x: x[1])[:5]

    # Print top 5 ETF recommendations for each method
    print("Top 5 ETF Recommendations (Cosine Similarity):")
    for i, (etf, score) in enumerate(cosine_top5):
        print(f"{i+1}. {etf['long_name']} ({etf['ticker']})")
        print(f"   {etf['summary']}")
        print(f"   Similarity Score: {score}")

    print("\nTop 5 ETF Recommendations (Euclidean Distance):")
    for i, (etf, score) in enumerate(euclidean_top5):
        print(f"{i+1}. {etf['long_name']} ({etf['ticker']})")
        print(f"   {etf['summary']}")
        print(f"   Distance: {score}")

    # print("\nTop 5 ETF Recommendations (Earth Mover's Distance):")
    # for i, (etf, score) in enumerate(emd_top5):
    #     print(f"{i+1}. {etf['long_name']} ({etf['ticker']})")
    #     print(f"   {etf['summary']}")
    #     print(f"   Distance: {score}")
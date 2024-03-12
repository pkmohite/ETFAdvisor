import json
import os
import numpy as np
from vertexai.language_models import TextEmbeddingModel
import thepassiveinvestor as pi

# Set the path to your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_key.json"

def get_embedding(text):
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    embeddings = model.get_embeddings([text])
    return embeddings[0].values

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def euclidean_distance(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.linalg.norm(a - b)

def dot_product(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b)

def manhattan_distance(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.sum(np.abs(a - b))

# Load the JSON data with embeddings from file
with open('etf_data_with_embeddings.json', 'r') as file:
    data = json.load(file)

# Get user input for investment strategy
user_input = input("Enter a description of the investment strategy: ")

# Generate embedding for user input
user_input_embedding = get_embedding(user_input)

# Calculate similarity using different algorithms
for etf in data:
    etf['cosine_similarity'] = cosine_similarity(user_input_embedding, etf['summary_embedding'])
    etf['euclidean_distance'] = euclidean_distance(user_input_embedding, etf['summary_embedding'])
    etf['dot_product'] = dot_product(user_input_embedding, etf['summary_embedding'])
    etf['manhattan_distance'] = manhattan_distance(user_input_embedding, etf['summary_embedding'])

# Sort ETFs based on each similarity algorithm
cosine_sorted_data = sorted(data, key=lambda x: x['cosine_similarity'], reverse=True)
euclidean_sorted_data = sorted(data, key=lambda x: x['euclidean_distance'])
dot_product_sorted_data = sorted(data, key=lambda x: x['dot_product'], reverse=True)
manhattan_sorted_data = sorted(data, key=lambda x: x['manhattan_distance'])

## Print top 5 ETF recommendations for each similarity algorithm
print("Top 5 ETF Recommendations (Cosine Similarity):")
for i in range(5):
    print(f"{i+1}. {cosine_sorted_data[i]['long_name']} ({cosine_sorted_data[i]['ticker']})")
    print(f"   Cosine Similarity: {cosine_sorted_data[i]['cosine_similarity']}")

print("\nTop 5 ETF Recommendations (Euclidean Distance):")
for i in range(5):
    print(f"{i+1}. {euclidean_sorted_data[i]['long_name']} ({euclidean_sorted_data[i]['ticker']})")
    print(f"   Euclidean Distance: {euclidean_sorted_data[i]['euclidean_distance']}")

print("\nTop 5 ETF Recommendations (Dot Product):")
for i in range(5):
    print(f"{i+1}. {dot_product_sorted_data[i]['long_name']} ({dot_product_sorted_data[i]['ticker']})")
    print(f"   Dot Product: {dot_product_sorted_data[i]['dot_product']}")

print("\nTop 5 ETF Recommendations (Manhattan Distance):")
for i in range(5):
    print(f"{i+1}. {manhattan_sorted_data[i]['long_name']} ({manhattan_sorted_data[i]['ticker']})")
    print(f"   Manhattan Distance: {manhattan_sorted_data[i]['manhattan_distance']}")

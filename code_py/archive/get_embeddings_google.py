import json
import os
from vertexai.language_models import TextEmbeddingModel

# Set the path to your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_key.json"

def get_embedding(text):
    if text is None:
        return None
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    embeddings = model.get_embeddings([text])
    return embeddings[0].values
    
# Load the JSON data from file
with open('etf_data.json', 'r') as file:
    data = json.load(file)

# Load only the first 10 ETFs
data = data[:10]

# Initialize an empty list to store the data
etf_strat = []


# Generate embeddings for each ETF
for i, etf in enumerate(data, start=1):
    try:
        item = {
            "ticker": etf['ticker'],
            "long_name": etf['long_name'],
            "summary": etf['summary'],
            "long_name_embedding": get_embedding(etf['long_name']),
            "summary_embedding": get_embedding(etf['summary'])
        }
        etf_strat.append(item)    
        print(f"Embeddings generated for ETF {i}: {etf['ticker']}")
    
    except KeyError as e:
        print(f"KeyError occurred for ETF {i}. Error: {str(e)}")
        print("Skipping to the next ETF...")
        continue

# Load existing data from etf_data.json file
try:
    with open('etf_data_with_embeddings_googlesample.json', 'r') as file:
        existing_data = json.load(file)
except FileNotFoundError:
    existing_data = []

# Append the new data to the existing data
existing_data.extend(etf_strat)

# Save the updated data structure to the etf_data.json file
with open('etf_data_with_embeddings_googlesample.json', 'w') as file:
    json.dump(existing_data, file, indent=4)

print("ETF data appended to etf_data_with_embeddings.json file.")
print("Number of ETFs processed:", len(existing_data))
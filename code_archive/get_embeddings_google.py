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

# Load only the first x ETFs
data = data[3080:]

# Initialize an empty list to store the data
etf_strat = []

# Initialize an empty list
existing_data = []  

# Generate embeddings for each ETF
for i, etf in enumerate(data, start=1):
    try:
        # Combine the ETF data into a single string
        ticker = etf['ticker'] if etf['ticker'] is not None else ''
        long_name = etf['long_name'] if etf['long_name'] is not None else ''
        summary = etf['summary'] if etf['summary'] is not None else ''
        text = ticker + ' ' + long_name + ' ' + summary
        
        # Create a dictionary to store the ETF data and its embedding
        item = {
            "ticker": etf['ticker'],
            "long_name": etf['long_name'],
            "summary": etf['summary'],
            "embedding": get_embedding(text)
        }
        # Append the dictionary to the list
        etf_strat.append(item)
        print(f"Embeddings generated for ETF {i}: {etf['ticker']}")

        # Append the new data to the existing data every 200 records
        if i % 20 == 0:
            
            # Load existing data from etf_data_with_embeddings.json file
            try:
                with open('etf_data_with_embeddings_v2.json', 'r') as file:
                    existing_data = json.load(file)
            except FileNotFoundError:
                existing_data = []
            
            # Append the new data to the existing data
            existing_data.extend(etf_strat)

            # Reset the list for the next batch
            etf_strat = []  

            # Save the updated data structure to the etf_data.json file
            with open('etf_data_with_embeddings_v2.json', 'w') as file:
                json.dump(existing_data, file, indent=4)
                
            # Print a message to indicate the progress
            print("ETF data appended to etf_data_with_embeddings.json file.")
            print("Number of ETFs processed:", len(existing_data))

        # Save the final batch of data to the etf_data_with_embeddings.json file
        if i == len(data):
            # Load existing data from etf_data_with_embeddings.json file
            try:
                with open('etf_data_with_embeddings_v2.json', 'r') as file:
                    existing_data = json.load(file)
            except FileNotFoundError:
                existing_data = []
            
            # Append the new data to the existing data
            existing_data.extend(etf_strat)

            # Save the updated data structure to the etf_data.json file
            with open('etf_data_with_embeddings_v2.json', 'w') as file:
                json.dump(existing_data, file, indent=4)
                
            # Print a message to indicate the progress
            print("ETF data appended to etf_data_with_embeddings.json file.")
            print("Number of ETFs processed:", len(existing_data))

    except KeyError as e:
        print(f"KeyError occurred for ETF {i}. Error: {str(e)}")
        print("Skipping to the next ETF...")
        continue
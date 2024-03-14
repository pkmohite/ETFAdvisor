from google.cloud import storage
import json
import os


# count tickers in etf_data_with_embeddings_v2.json file in local
with open('etf_data_with_embeddings_v2.json', 'r') as file:
    data = json.load(file)


# %%
class GCSFileManager:
    def __init__(self, key_file_path):
        # Set the path to the Google Cloud service account key file
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_file_path
        self.client = storage.Client()

    def import_json_from_gcs(self, bucket_name, file_name):
        # Get the bucket
        bucket = self.client.get_bucket(bucket_name)

        # Get the blob (file) from the bucket
        blob = bucket.blob(file_name)

        # Download the blob as a string
        json_string = blob.download_as_text()

        # Parse the JSON string
        json_data = json.loads(json_string)

        return json_data

    def update_json_in_gcs(self, bucket_name, file_name, json_data):
        # Get the bucket
        bucket = self.client.get_bucket(bucket_name)

        # Get the blob (file) from the bucket
        blob = bucket.blob(file_name)

        # Convert the JSON data to a string
        json_string = json.dumps(json_data, indent=4)

        # Upload the string to the blob
        blob.upload_from_string(json_string)

        print(f"JSON data updated in the file {file_name} in the bucket {bucket_name}")

# Usage example
bucket_name = "etf_repo"
file_name = "sample_portfolio.json"
key_file_path = "google_key.json"

gcs_file_manager = GCSFileManager(key_file_path)
json_data = gcs_file_manager.import_json_from_gcs(bucket_name, file_name)

# Print the JSON data
print(json_data)


    
import thepassiveinvestor as pi
import json
from etfpy import ETF, load_etf, get_available_etfs_list
import os

# Load the ETF tickers from the JSON file
with open('etf_tickers.json', 'r') as file:
    etf_tickers_all = json.load(file)

# Take the tickers from index x to y (inclusive) from the loaded list
etf_tickers = etf_tickers_all[2501:]

# Initialize an empty list to store the data
etf_strat = []

# Collect data for each selected ticker
for ticker in etf_tickers:
    try:
        etf_data = pi.collect_data(ticker)
        item = {
            "ticker": ticker,
            "long_name": etf_data["long_name"],
            "summary": etf_data["summary"]
        }
        etf_strat.append(item)
        print(f"Data collected for ticker: {ticker}")
    except KeyError as e:
        print(f"KeyError occurred for ticker: {ticker}. Error: {str(e)}")
        print("Skipping to the next ticker...")
        continue

# Load existing data from etf_data.json file
try:
    with open('etf_data.json', 'r') as file:
        existing_data = json.load(file)
except FileNotFoundError:
    existing_data = []

# Append the new data to the existing data
existing_data.extend(etf_strat)

# Save the updated data structure to the etf_data.json file
with open('etf_data.json', 'w') as file:
    json.dump(existing_data, file, indent=4)

print("ETF data appended to etf_data.json file.")
print("Number of ETFs processed:", len(existing_data))
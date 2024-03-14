import json

# import etf_data_with _embeddings_v2.json fro local directory
with open('etf_data_with_embeddings_v2.json') as f:
    data = json.load(f)

# create a list of keywords of popular ETF companies like BlackRock, Vanguard, etc.
etf_companies_short = ['BlackRock', 'Vanguard']

# create a list of keywords of popular ETF companies like BlackRock, Vanguard, etc.
etf_companies = ['BlackRock', 'Vanguard', 'State Street', 'Invesco', 'VanEck', 'WisdomTree',  'JPMorgan',  'Fidelity', 'iShares', 'SPDR', 'Schwab']

# parse data to find the ETF companies if etf_companies keywords are a part of the long_name of the ETF
etf_companies_data = []
for etf in data:
    if 'long_name' in etf and etf['long_name'] is not None:
        for company in etf_companies:
            if company in etf['long_name']:
                etf_companies_data.append(etf)
                break

# save the data in a JSON file
with open('etf_data_short.json', 'w') as f:
    json.dump(etf_companies_data, f)

# print the length of the data
print(len(etf_companies_data))

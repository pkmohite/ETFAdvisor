import pandas as pd
import json
import streamlit as st
import webbrowser

# Load the JSON data from the file
with open('sample_portfolio.json') as file:
    portfolio_data = json.load(file)

# Extract all bucket and asset data into a DataFrame
data_all = []
for bucket in portfolio_data['buckets']:
    bucket_name = bucket['name']
    bucket_target_ratio = bucket['target_ratio']
    for asset in bucket['assets']:
        ticker = asset['ticker']
        name = asset['name']
        target_ratio = asset['target_ratio']
        data_all.append([bucket_name, bucket_target_ratio, ticker, name, target_ratio])

# Extract the relevant data from data_all into a DataFrame
df = pd.DataFrame(data_all, columns=['Bucket Name', 'Bucket Target Ratio', 'Ticker', 'Asset Name', 'Asset Target Ratio'])

### Streamlit Components

# Define wide container
st.set_page_config(layout="wide")

# Title as the "portfolio_description" from the JSON file
st.title(portfolio_data['portfolio_description'])

# Display data only
show_df = st.write(df)

# New Title: Features
st.subheader('Features')

#add buttons: Add New Bucket, Add Asset to Existing Bucket
add_new_bucket = st.button('Add New Bucket')
add_asset_to_existing_bucket = st.button('Add Asset to Existing Bucket')

# if add_new_bucket:clicked then display the form to add new bucket
if add_new_bucket:
    st.subheader('Add New Bucket')
    bucket_name = st.text_input('Bucket Name')
    bucket_target_ratio = st.number_input('Bucket Target Ratio', min_value=0.0, max_value=100.0, value=0.0)
    add_bucket = st.button('Add Bucket')

# if add_asset_to_existing_bucket:clicked then display the form to add asset to existing bucket
if add_asset_to_existing_bucket:
    st.subheader('Add Asset to Existing Bucket')
    selected_bucket = st.selectbox('Select a Bucket', df['Bucket Name'].unique())
    asset_target_ratio = st.number_input('Asset Target Ratio', min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    selected_asset = st.text_area('Describe your strategy')
    get_recommendation = st.button('Get ETF Recommendation')

    # if get_recommendation is clicked, open google.com
    if get_recommendation:
        st.markdown('[Click here for the recommendation](https://www.google.com)', unsafe_allow_html=True)


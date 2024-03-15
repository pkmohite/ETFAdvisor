#st_allocation.py
import streamlit as st
from st_rebalance import rebalance_portfolio
import json

def load_portfolio():
    with open('portfolio.json', 'r') as file:
        portfolio = json.load(file)
    return portfolio

def save_portfolio(portfolio):
    with open('portfolio.json', 'w') as file:
        json.dump(portfolio, file, indent=2)

def change_etf_allocation(portfolio):
    st.header('Change ETF Allocation')
    selected_bucket = st.selectbox('Select a bucket', [bucket['name'] for bucket in portfolio['buckets']])

    for bucket in portfolio['buckets']:
        if bucket['name'] == selected_bucket:
            st.subheader(f"{bucket['name']} Bucket")
            etf_allocations = {etf['ticker']: etf['allocation'] for etf in bucket['etfs']}

            new_allocations = {}
            for etf in bucket['etfs']:
                ticker = etf['ticker']
                new_allocations[ticker] = st.number_input(f"New allocation for {ticker} (%)", value=float(etf_allocations[ticker]), min_value=0.0, max_value=100.0, step=0.1)

            if st.button('Rebalance'):
                total_allocation = sum(new_allocations.values())
                if total_allocation != 100:
                    st.error('Total allocation must sum up to 100%')
                else:
                    portfolio = rebalance_portfolio(portfolio, selected_bucket, new_allocations)
                    return portfolio

    return None

# Set the page layout to wide
st.set_page_config(layout="wide")

portfolio = load_portfolio()

updated_portfolio = change_etf_allocation(portfolio)
if updated_portfolio:
    save_portfolio(updated_portfolio)
    st.success('Portfolio updated successfully!')

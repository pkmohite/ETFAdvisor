# file: st_app/st_edit_bucket.py
import streamlit as st
from st_rebalance_etfs import rebalance_etfs_old, rebalance_etfs
import json
from st_home import fetch_current_price, load_portfolio, save_portfolio


portfolio = load_portfolio()
st.header('Change Bucket Allocation')
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
                portfolio = rebalance_etfs(portfolio, selected_bucket, new_allocations)
                if portfolio is not None:
                    save_portfolio(portfolio)
                st.success('Portfolio updated successfully!')
                break

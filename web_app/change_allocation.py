import streamlit as st
from rebalance import rebalance_portfolio

def change_etf_allocation(portfolio):
    st.header('Change ETF Allocation')

    selected_bucket = st.selectbox('Select a bucket', [bucket['name'] for bucket in portfolio['buckets']])

    bucket = next(b for b in portfolio['buckets'] if b['name'] == selected_bucket)

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
            if new_allocations != etf_allocations:
                portfolio = rebalance_portfolio(portfolio, selected_bucket, new_allocations)
                return portfolio
            else:
                st.warning('No changes made to the portfolio.')

    return None
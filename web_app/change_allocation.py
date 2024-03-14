import streamlit as st
from home import fetch_current_price

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
                    # Emulate selling all ETFs in the bucket
                    total_value = sum(fetch_current_price(etf['ticker']) * etf['shares'] for etf in bucket['etfs'])
                    total_value += portfolio['cash']

                    # Emulate buying ETFs based on the new allocations
                    for etf in bucket['etfs']:
                        ticker = etf['ticker']
                        new_allocation = new_allocations[ticker] / 100
                        target_amount = total_value * new_allocation
                        current_price = fetch_current_price(ticker)
                        if current_price is not None:
                            new_shares = int(target_amount / current_price)  # Round down to the nearest integer
                            etf['shares'] = new_shares
                            etf['allocation'] = new_allocations[ticker]

                    # Update the cash amount after rebalancing
                    portfolio['cash'] = total_value - sum(fetch_current_price(etf['ticker']) * etf['shares'] for etf in bucket['etfs'])

                    return portfolio

    return None
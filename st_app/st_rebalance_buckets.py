# file: st_app/st_rebalance_buckets.py
import streamlit as st
import json
from st_home import fetch_current_price, load_portfolio, save_portfolio, calculate_total_value
from st_rebalance_etfs import rebalance_etfs

def rebalance_buckets(portfolio, new_allocations):

    # Update  portfolio with the new allocations
    for bucket in portfolio['buckets']:
        bucket_name = bucket['name']
        bucket['allocation'] = new_allocations[bucket_name]

    # Store the total value of the portfolio
    total_value = calculate_total_value(portfolio)

    # Loop through the buckets and loop through the ETFs in each bucket
    for bucket in portfolio['buckets']:
        for etf in bucket['etfs']:
            ticker = etf['ticker']
            current_price = fetch_current_price(ticker)
            if current_price is not None:
                overall_allocation = bucket['allocation'] * etf['allocation'] / 100
                target_amount = total_value * overall_allocation / 100
                new_shares = int(target_amount / current_price)
                etf['shares'] = new_shares

    # Update the cash amount after rebalancing
    total_ETF_value = 0
    for bucket in portfolio['buckets']:
        for etf in bucket['etfs']:
            total_ETF_value += fetch_current_price(etf['ticker']) * etf['shares']
    portfolio['cash'] = total_value - total_ETF_value

    # Return the updated portfolio
    return portfolio
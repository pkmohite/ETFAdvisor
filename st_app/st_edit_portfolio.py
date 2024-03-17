# file: st_app/st_edit_portfolio.py
import streamlit as st
import json
from st_rebalance_buckets import rebalance_buckets
from st_home import load_portfolio, save_portfolio


st.header('Edit Bucket Allocation')

portfolio = load_portfolio()

current_cash = portfolio['cash']
st.write(f"Current Cash: ${current_cash:.2f}")

new_allocations = {}

for bucket in portfolio['buckets']:
    bucket_name = bucket['name']
    current_allocation = bucket['allocation']
    new_allocation = st.number_input(f"{bucket_name} Allocation (%)", value=float(current_allocation), min_value=0.0, max_value=100.0, step=0.1)
    new_allocations[bucket_name] = new_allocation

if st.button('Save Allocation'):
    total_allocation = sum(new_allocations.values())
    if total_allocation != 100:
        st.error('Total allocation must sum up to 100%')
    else:
        portfolio = rebalance_buckets(portfolio, new_allocations)
        save_portfolio(portfolio)
        st.success('Portfolio updated successfully!')
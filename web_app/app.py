import streamlit as st
import json
from home import display_portfolio
from change_allocation import change_etf_allocation
from etf_recommender import etf_recommender_page

def load_portfolio():
    with open('portfolio.json', 'r') as file:
        portfolio = json.load(file)
    return portfolio

def save_portfolio(portfolio):
    with open('portfolio.json', 'w') as file:
        json.dump(portfolio, file, indent=2)

def main():
    st.set_page_config(page_title='Portfolio Manager', layout='wide')
    portfolio = load_portfolio()

    st.sidebar.title('Navigation')
    page = st.sidebar.radio('Go to', ['Home', 'Change ETF Allocation', 'ETF Recommender'])

    if page == 'Home':
        display_portfolio(portfolio)
    elif page == 'Change ETF Allocation':
        updated_portfolio = change_etf_allocation(portfolio)
        if updated_portfolio:
            save_portfolio(updated_portfolio)
            st.sidebar.success('Portfolio updated successfully!')
    elif page == 'ETF Recommender':
        etf_recommender_page()

if __name__ == '__main__':
    main()
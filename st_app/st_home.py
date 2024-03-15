#st_home.py
import streamlit as st
import yfinance as yf
import json

def load_portfolio():
    with open('portfolio.json', 'r') as file:
        portfolio = json.load(file)
    return portfolio

def fetch_current_price(ticker):
    stock = yf.Ticker(ticker)
    if 'currentPrice' in stock.info:
        return stock.info['currentPrice']
    elif 'regularMarketPrice' in stock.info:
        return stock.info['regularMarketPrice']
    elif 'ask' in stock.info:
        return stock.info['ask']
    elif 'bid' in stock.info:
        return stock.info['bid']
    else:
        return None

def display_portfolio():
    st.header('Your Portfolio')
    st.subheader('Cash')

    portfolio = load_portfolio()

    st.write(f"Available Cash: ${portfolio['cash']:.2f}")

    for bucket in portfolio['buckets']:
        st.subheader(bucket['name'])
        st.write(f"Allocation: {bucket['allocation']}%")

        etf_data = []
        for etf in bucket['etfs']:
            ticker = etf['ticker']
            current_price = fetch_current_price(ticker)
            if current_price is not None:
                total_value = current_price * etf['shares']
                etf_data.append([ticker, etf['allocation'], etf['shares'], current_price, total_value])
            else:
                etf_data.append([ticker, etf['allocation'], etf['shares'], 'N/A', 'N/A'])

        columns = ['Ticker', 'Allocation', 'Shares', 'Current Price', 'Total Value']
        st.table(etf_data)

display_portfolio()
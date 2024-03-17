# file: st_app/st_home.py
import streamlit as st
import yfinance as yf
import json
import pandas as pd

def load_portfolio():
    with open('portfolio.json', 'r') as file:
        portfolio = json.load(file)
    return portfolio

def save_portfolio(portfolio):
    with open('portfolio.json', 'w') as file:
        json.dump(portfolio, file, indent=2)


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

# function to fetch ETF Name
def fetch_etf_name(ticker):
    stock = yf.Ticker(ticker)
    return stock.info['longName']

def calculate_total_value(portfolio):
    # determine the total value of all the buckets
    total_value = 0
    for bucket in portfolio['buckets']:
        for etf in bucket['etfs']:
            total_value += fetch_current_price(etf['ticker']) * etf['shares']
    # Add the cash amount to the total value
    total_value += portfolio['cash']
    return total_value


def display_portfolio():
    portfolio = load_portfolio()

    st.header('Your Portfolio')
    st.write(f"Total Value: ${float(calculate_total_value(portfolio)):.2f} USD")
    st.write(f"Investable Cash: ${portfolio['cash']:.2f}")

    for bucket in portfolio['buckets']:
        st.subheader(bucket['name'])
        st.write(f"Allocation: {bucket['allocation']}%")

        etf_data = []
        for etf in bucket['etfs']:
            ticker = etf['ticker']
            etf_name = fetch_etf_name(ticker)
            current_price = fetch_current_price(ticker)
            if current_price is not None:
                total_value = current_price * etf['shares']
                etf_data.append([ticker, etf_name, etf['allocation'], etf['shares'], f"$ {current_price}", f"$ {total_value}"])
            else:
                etf_data.append([ticker, etf_name, etf['allocation'], etf['shares'], 'N/A', 'N/A'])

        etf_df = pd.DataFrame(etf_data, columns=['Ticker', 'Name', 'Allocation', 'Shares', 'Current Price', 'Total Value'])
        st.dataframe(etf_df,use_container_width=True)

st.set_page_config(layout="wide")
display_portfolio()
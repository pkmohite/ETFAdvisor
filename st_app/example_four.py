import streamlit as st
from st_pages import add_page_title, hide_pages

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

add_page_title()

st.subheader('Cash')

selection = st.radio(
    "Test page hiding",
    ["Show all pages", "Hide pages 1 and 2", "Hide Other apps Section"],
)

if selection == "Show all pages":
    hide_pages([])
elif selection == "Hide pages 1 and 2":
    hide_pages(["Example One", "Example Two"])
elif selection == "Hide Other apps Section":
    hide_pages(["Other apps"])

st.selectbox("test_select", options=["1", "2", "3"])

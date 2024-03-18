# file: st_app/st_app.py
from pathlib import Path
import streamlit as st
from st_pages import Page, add_page_title, show_pages

st.set_page_config(layout="wide")

with st.echo("below"):

    show_pages(
        [
            Page("st_app/st_home.py", "Your Portfolio", "💰"),
            Page("st_app/st_edit_bucket.py", "Change Bucket Allocation", "🪣"),
            Page("st_app/st_edit_portfolio.py", "Rebalance Portfolio", "🔄"),
            Page("st_app/st_search_ETFs.py", "ETF Recommender", "📖"),
        ]
    )

    add_page_title()  # Optional method to add title and icon to current page

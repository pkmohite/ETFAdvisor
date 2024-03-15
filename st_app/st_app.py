# st_app.py
from pathlib import Path
import streamlit as st


with st.echo("below"):
    from st_pages import Page, add_page_title, show_pages

    "## Declaring the pages in your app:"

    show_pages(
        [
            Page("st_app/st_home.py", "Your Portfolio", "💰"),  
            Page("st_app/st_allocation.py", "Change Bucket Allocation", "🪣"),
            Page("st_app/st_recommender.py", "ETF Recommender", "📖"),
        ]
    )
    
    add_page_title()  # Optional method to add title and icon to current page


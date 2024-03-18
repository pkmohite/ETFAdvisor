# file: st_app/st_search_ETFs.py
import streamlit as st
import json
import numpy as np
import pandas as pd
from st_recommender import ETFRecommender
from config import column_config_recc
from st_home import load_portfolio, save_portfolio, fetch_etf_details
from st_rebalance_buckets import rebalance_buckets

# Function Definitions

def recommend_etfs(new_allocation):
    recommender = ETFRecommender()
    recommendations = recommender.recommend_etfs(new_allocation)
    recommendations = pd.DataFrame(recommendations)

    # Fetch ETF details for each ticker symbol
    etf_details = pd.DataFrame(
        [fetch_etf_details(ticker) for ticker in recommendations["ticker"]]
    )
    # Add a checkbox to the start of recommendations
    recommendations.insert(0, "add", False)
    # add a % allocation column to recommendations
    recommendations["allocation"] = 0.0
    # From etf_details add the following to recommendations: "totalAssets", "category", "threeYearAverageReturn", "fiveYearAverageReturn"
    recommendations["threeYearAverageReturn"] = (
        etf_details["threeYearAverageReturn"] * 100
    )
    recommendations["fiveYearAverageReturn"] = (
        etf_details["fiveYearAverageReturn"] * 100
    )
    recommendations["totalAssets"] = etf_details["totalAssets"] / 1000000
    recommendations["category"] = etf_details["category"]
    recommendations = recommendations.drop(
        columns=["embedding", "similarity", "summary"]
    )

    # arrange the columns in the order of column_config_recc
    recommendations = recommendations[column_config_recc.keys()]

    return recommendations

def add_bucket(portfolio, selected_etfs, bucket_allocation):
    # Scale down the allocation of other buckets to make room for the new bucket
    total_allocation = sum([bucket["allocation"] for bucket in portfolio["buckets"]])
    scaling_factor = (100 - bucket_allocation) / total_allocation
    for bucket in portfolio["buckets"]:
        bucket["allocation"] *= scaling_factor
    # Add the new bucket to the portfolio
    new_bucket = {
        "name": "New Bucket",
        "allocation": bucket_allocation,
        "etfs": selected_etfs.to_dict(orient="records"),
    }
    portfolio["buckets"].append(new_bucket)
    
    # rebalance the buckets using the new scaled allocation
    portfolio = rebalance_buckets(
        portfolio,
        {bucket["name"]: bucket["allocation"] for bucket in portfolio["buckets"]},
    )

    return portfolio

# Session State

if 'clicked' not in st.session_state:
    st.session_state.clicked = False


def click_button():
    st.session_state.clicked = True

# Streamlit App

st.header("ETF Recommender")
strategy_desc = st.text_area("Describe your ETF Strategy")
st.session_state.clicked = False
st.button("AI ETF Search", on_click=click_button())

if st.session_state.clicked:
    # Get ETF recommendations and display in a st.dataframe
    if strategy_desc != "":
        recommendations = recommend_etfs(strategy_desc)
        edited_df = st.data_editor(
            recommendations,
            hide_index=True,
            use_container_width=True,
            column_config=column_config_recc,
        )
        # Single Input field for allocation percentage
        bucket_allocation = st.number_input(
            "Allocation for the bucket (%)",
            value=0.0,
            min_value=0.0,
            max_value=100.0,
            step=0.1,
        )
        # Display Selected ETFs
        # selected_etfs = pd.DataFrame()
        # selected_etfs = selected_etfs._append(edited_df[edited_df["add"] == True])
        # selected_etfs = st.dataframe(
        #     selected_etfs,
        #     hide_index=True,
        #     use_container_width=True,
        #     column_config=column_config_recc,
        # )
        # Add button to add selected ETFs
        if st.button("Add Selected ETFs"):
            # Get the selected ETFs
            selected_etfs = pd.DataFrame()
            selected_etfs = selected_etfs._append(edited_df[edited_df["add"] == True])
            # Check if the total allocation is 100%
            total_allocation = selected_etfs["allocation"].sum()
            if total_allocation != 100:
                st.error("Total allocation must sum up to 100%")
            else:
                new_allocations = {
                    ticker: allocation
                    for ticker, allocation in zip(
                        selected_etfs["ticker"], selected_etfs["allocation"]
                    )
                }

                # Load the portfolio
                portfolio = load_portfolio()
                # Add the selected ETFs as a new bucket to the portfolio
                portfolio = add_bucket(portfolio, selected_etfs, bucket_allocation)
                if portfolio is not None:
                    save_portfolio(portfolio)
                st.success("Portfolio updated successfully!")

    else:
        st.error(
            "Description is empty! Please enter a description of the investment strategy."
        )

        

    
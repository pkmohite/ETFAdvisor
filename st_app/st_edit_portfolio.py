# file: st_app/st_edit_portfolio.py
import streamlit as st
import json
from config import column_config_recc
from st_home import (
    fetch_current_price,
    load_portfolio,
    save_portfolio,
    fetch_etf_details,
)
from st_rebalance_etfs import rebalance_etfs_old, rebalance_etfs
from st_recommender import ETFRecommender
from st_rebalance_buckets import rebalance_buckets
import pandas as pd
from config import static_bucket

if "button" not in st.session_state:
    st.session_state.button = False


def click_button():
    st.session_state.button = not st.session_state.button


if "button2" not in st.session_state:
    st.session_state.button2 = False


def click_button_2():
    st.session_state.button2 = not st.session_state.button2


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
    # Add the selected ETFs as a new bucket to the portfolio
    new_bucket = {
        "name": "New Bucket",
        "allocation": bucket_allocation,
        "etfs": selected_etfs.to_dict(orient="records"),
    }
    portfolio["buckets"].append(new_bucket)

    # Scale down the allocation of other buckets to make room for the new bucket
    total_allocation = sum([bucket["allocation"] for bucket in portfolio["buckets"]])
    scaling_factor = (100 - bucket_allocation) / total_allocation
    for bucket in portfolio["buckets"]:
        bucket["allocation"] *= scaling_factor

    # rebalance the buckets using the new scaled allocation
    portfolio = rebalance_buckets(
        portfolio,
        {bucket["name"]: bucket["allocation"] for bucket in portfolio["buckets"]},
    )

    return portfolio


## Streamlit App
st.header("Edit Bucket Allocation")

portfolio = load_portfolio()

current_cash = portfolio["cash"]
st.write(f"Current Cash: ${current_cash:.2f}")

new_allocations = {}

for bucket in portfolio["buckets"]:
    bucket_name = bucket["name"]
    current_allocation = bucket["allocation"]
    new_allocation = st.number_input(
        f"{bucket_name} Allocation (%)",
        value=float(current_allocation),
        min_value=0.0,
        max_value=100.0,
        step=0.1,
    )
    new_allocations[bucket_name] = new_allocation

col1, col2 = st.columns([0.13, 1])
if col1.button("Save Allocation"):
    total_allocation = sum(new_allocations.values())
    if total_allocation != 100:
        col1.error("Total allocation must sum up to 100%")
    else:
        portfolio = rebalance_buckets(portfolio, new_allocations)
        save_portfolio(portfolio)
        col1.success("Portfolio updated successfully!")

col2.button("Add New ETF", on_click=click_button)

if st.session_state.button:
    st.subheader("Add New ETF")
    strategy_desc = st.text_area(
        "Describe your ETF Strategy", value=st.session_state.get("key", "")
    )
    st.button("AI ETF Search", on_click=click_button_2)
    if st.session_state.button2:
        if strategy_desc is not None:
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

        # Check if recommendations table is edited
        if edited_df is not None:
            recommendations = edited_df

        # Add button to add selected ETFs
        if st.button("Add Selected ETFs"):
            # Add ticker and allocation columns of selected ETFs into a dictionary
            selected_etfs = recommendations[recommendations["add"] == True]
            selected_etfs = selected_etfs[["ticker", "allocation"]]

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

                # Add the selected ETFs as a new bucket to the portfolio
                portfolio = add_bucket(portfolio, selected_etfs, bucket_allocation)
                if portfolio is not None:
                    save_portfolio(portfolio)
                st.success("Portfolio updated successfully!")

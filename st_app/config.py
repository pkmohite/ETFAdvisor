import streamlit as st
from datetime import date

column_config_home = {
    "ticker": st.column_config.TextColumn(
        "Ticker", help="The ticker symbol of the investment"
    ),
    "name": st.column_config.TextColumn("Name", help="The name of the investment"),
    "allocation": st.column_config.NumberColumn(
        "Allocation",
        min_value=0,
        max_value=100,
        format="%d%%",
        help="The allocation percentage of the investment",
    ),
    "shares": st.column_config.NumberColumn(
        "Shares",
        min_value=0,
        format="%d",
        help="The number of shares of the investment",
    ),
    "current_price": st.column_config.NumberColumn(
        "Current Price",
        min_value=0,
        format="$%.2f",
        help="The current price of the investment",
    ),
    "total_value": st.column_config.NumberColumn(
        "Total Value",
        min_value=0,
        format="$%.2f",
        help="The total value of the investment",
    ),
}

column_config_recc = {
    "add": st.column_config.CheckboxColumn("Add", help="Add recommendation"),
    "allocation": st.column_config.NumberColumn(
        "Allocation (%)",
        min_value=0.0,
        max_value=100.0,
        step=0.1,
        format="%.1f%%",
        help="The allocation percentage for each ETF",
    ),
    "ticker": st.column_config.TextColumn(
        "Ticker", help="The ticker symbol of the recommendation"
    ),
    "category": st.column_config.TextColumn("Category", help="The category of the ETF"),
    "long_name": st.column_config.TextColumn(
        "ETF Name", help="The name of the recommendation"
    ),
    "threeYearAverageReturn": st.column_config.NumberColumn(
        "3-Year Avg Return",
        min_value=0.0,
        max_value=100.0,
        format="%.2f%%",
        help="The three-year average return of the ETF",
    ),
    "fiveYearAverageReturn": st.column_config.NumberColumn(
        "5-Year Avg Return",
        min_value=0.0,
        max_value=100.0,
        format="%.2f%%",
        help="The five-year average return of the ETF",
    ),
    "totalAssets": st.column_config.NumberColumn(
        "Total Assets",
        min_value=0.0,
        format="$%.2f M",
        help="The total assets of the ETF",
    ),
}

column_configuration = {
    "name": st.column_config.TextColumn(
        "Name", help="The name of the user", max_chars=100
    ),
    "avatar": st.column_config.ImageColumn("Avatar", help="The user's avatar"),
    "active": st.column_config.CheckboxColumn("Is Active?", help="Is the user active?"),
    "homepage": st.column_config.LinkColumn(
        "Homepage", help="The homepage of the user"
    ),
    "gender": st.column_config.SelectboxColumn(
        "Gender", options=["male", "female", "other"]
    ),
    "age": st.column_config.NumberColumn(
        "Age",
        min_value=0,
        max_value=120,
        format="%d years",
        help="The user's age",
    ),
    "activity": st.column_config.LineChartColumn(
        "Activity (1 year)",
        help="The user's activity over the last 1 year",
        width="large",
        y_min=0,
        y_max=100,
    ),
    "daily_activity": st.column_config.BarChartColumn(
        "Activity (daily)",
        help="The user's activity in the last 25 days",
        width="medium",
        y_min=0,
        y_max=1,
    ),
    "status": st.column_config.ProgressColumn(
        "Status", min_value=0, max_value=1, format="%.2f"
    ),
    "birthdate": st.column_config.DateColumn(
        "Birthdate",
        help="The user's birthdate",
        min_value=date(1920, 1, 1),
    ),
    "email": st.column_config.TextColumn(
        "Email",
        help="The user's email address",
        validate="^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$",
    ),
}

static_bucket = {
    "name": "",
    "allocation": 0.0,
    "etfs": [
        {"ticker": "BND", "allocation": 50.0, "shares": 0},
        {"ticker": "VTI", "allocation": 50.0, "shares": 0},
    ],
}

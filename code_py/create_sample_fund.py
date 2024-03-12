import json
import os

# Sample JSON data
sample_data = {
    "portfolio_description": "{{name}}'s Portfolio",
    "cash": {
        "amount": 10000,
        "target_ratio": 0.2
    },
    "buckets": [
        {
            "name": "Retirement",
            "description": "Bucket focused on stable, long-term growth for retirement",
            "risk_profile": "Moderate Risk",
            "target_ratio": 0.5,
            "annualized_return": 0.06,
            "assets": [
                {
                    "ticker": "VGIT",
                    "name": "Vanguard Intermediate-Term Treasury ETF",
                    "description": "ETF investing in U.S. Treasury bonds with intermediate-term maturities",
                    "target_ratio": 0.6,
                    "num_shares": 100,
                    "annualized_return": 0.04
                },
                {
                    "ticker": "VGLT",
                    "name": "Vanguard Long-Term Treasury ETF",
                    "description": "ETF investing in U.S. Treasury bonds with long-term maturities",
                    "target_ratio": 0.4,
                    "num_shares": 75,
                    "annualized_return": 0.05
                }
            ]
        },
        {
            "name": "Growth",
            "description": "Bucket focused on higher-risk, higher-growth investments",
            "risk_profile": "High Risk",
            "target_ratio": 0.3,
            "annualized_return": 0.10,
            "assets": [
                {
                    "ticker": "QQQ",
                    "name": "Invesco QQQ Trust",
                    "description": "ETF tracking the Nasdaq-100 Index, comprised of large-cap tech companies",
                    "target_ratio": 0.5,
                    "num_shares": 50,
                    "annualized_return": 0.12
                },
                {
                    "ticker": "ARKK",
                    "name": "ARK Innovation ETF",
                    "description": "ETF investing in companies driving disruptive innovation",
                    "target_ratio": 0.5,
                    "num_shares": 80,
                    "annualized_return": 0.15
                }
            ]
        }
    ]
}

# Prompt the user for their name
name = input("Enter your name: ")

# Update the portfolio description with the user's name
sample_data["portfolio_description"] = sample_data["portfolio_description"].replace("{{name}}", name)

# Save the sample data to a JSON file
file_path = "sample_portfolio.json"
with open(file_path, "w") as file:
    json.dump(sample_data, file, indent=2)

print(f"Congrats! Your sample portfolio has been created")
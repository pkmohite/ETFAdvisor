# ETFAdvisor

An AI-powered ETF portfolio management tool built with Python and Streamlit. Get personalized ETF recommendations using natural language and manage your portfolio with real-time data.

## Features

- **AI ETF Recommendations**: Describe your investment strategy in plain English and get relevant ETF suggestions
- **Portfolio Management**: Track your investments with real-time pricing from Yahoo Finance
- **Bucket Organization**: Group ETFs into themes (Conservative, Growth, etc.)
- **Rebalancing Tools**: Automatically calculate trades needed to reach target allocations

## Project Structure

```
ETFAdvisor/
├── st_app/           # Main Streamlit application
├── ETF_recommender/  # Core recommendation engine  
├── portfolio.json    # Your portfolio data
└── etf_data_short.json # ETF database with AI embeddings
```

## Quick Start

1. **Install dependencies**
   ```bash
   pip install -r st_app/requirements.txt
   ```

2. **Set up Google Cloud**
   - Create a service account in Google Cloud Console
   - Download the key as `google_key.json` in the project root
   - Enable Vertex AI API

3. **Run the app**
   ```bash
   cd st_app
   streamlit run st_app.py
   ```

## How to Use

### Get ETF Recommendations
1. Go to "ETF Recommender" page
2. Describe your investment strategy: 
   - "Growth stocks for long-term investing"
   - "Conservative dividend ETFs for retirement"
3. Review top 5 recommendations
4. Add selected ETFs to your portfolio

### Manage Your Portfolio
- **Portfolio Overview**: See current holdings and performance
- **Change Bucket Allocation**: Adjust high-level investment themes
- **Rebalance Portfolio**: Fine-tune individual ETF weights

## Tech Stack

- **Python**: Core application language
- **Streamlit**: Web interface
- **Google Vertex AI**: Text embeddings for recommendations
- **Yahoo Finance**: Real-time ETF data

## Disclaimer

This tool is for educational purposes only. Not financial advice. Always consult professionals before making investment decisions.
# Setup Guide

## Requirements

- Python 3.8+
- Google Cloud account (free tier works)
- Internet connection

## Installation Steps

### 1. Clone and Install
```bash
git clone https://github.com/pkmohite/ETFAdvisor.git
cd ETFAdvisor
pip install -r st_app/requirements.txt
```

### 2. Google Cloud Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use existing)
3. Enable "Vertex AI API"
4. Create a service account with "Vertex AI User" role
5. Download the service account key as JSON
6. Rename it to `google_key.json` and place in project root

### 3. Run the App
```bash
cd st_app
streamlit run st_app.py
```

Open `http://localhost:8501` in your browser.

## Troubleshooting

**Google Cloud Authentication Error**: Check that `google_key.json` is in the project root.

**Module Import Errors**: Make sure you installed requirements: `pip install -r st_app/requirements.txt`

**Port Already in Use**: Stop other Streamlit processes or use: `streamlit run st_app.py --server.port 8502`

**Yahoo Finance Issues**: Check your internet connection.

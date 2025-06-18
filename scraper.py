import requests
import streamlit as st

def scrape_jobs(query):
    api_key = st.secrets.get("SERPAPI_KEY")
    if not api_key:
        st.error("Missing SerpAPI key in secrets.")
        return []

    params = {
        "engine": "google_jobs",
        "q": query,
        "hl": "en",
        "api_key": api_key
    }

    try:
        res = requests.get("https://serpapi.com/search", params=params)
        data = res.json()

        return data.get("jobs_results", [])
    except Exception as e:
        st.error(f"Scraping failed: {e}")
        return []

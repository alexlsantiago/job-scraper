import requests
import streamlit as st

def scrape_jobs(query, location):
    api_key = st.secrets.get("SERPAPI_KEY")
    if not api_key:
        st.error("Missing SerpAPI key in secrets.")
        return []

    params = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "hl": "en",
        "api_key": api_key
    }

    try:
        res = requests.get("https://serpapi.com/search", params=params)
        data = res.json()
        jobs = data.get("jobs_results", [])

        # Attempt to clean and standardize the job links
        for job in jobs:
            # If there are any external links, use them
            if "related_links" in job and job["related_links"]:
                job["external_link"] = job["related_links"][0].get("link", job.get("link"))
            else:
                job["external_link"] = job.get("link")

        return jobs
    except Exception as e:
        st.error(f"Scraping failed: {e}")
        return []

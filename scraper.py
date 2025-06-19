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
        raw_jobs = data.get("jobs_results", [])
        
        # Normalize fields to avoid missing data
        jobs = []
        for job in raw_jobs:
            jobs.append({
                "title": job.get("title", "No title"),
                "company": job.get("company_name", "Not available"),
                "location": job.get("location", "Not available"),
                "snippet": job.get("description", "Not available"),
                "link": job.get("related_links", [{}])[0].get("link", job.get("job_id", "#"))
            })

        return jobs

    except Exception as e:
        st.error(f"Scraping failed: {e}")
        return []

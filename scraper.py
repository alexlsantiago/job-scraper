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
        
        jobs = []
        for job in raw_jobs:
            # Try to extract a usable job link
            apply_link = None

            # Option 1: SerpAPI detected extensions
            if "detected_extensions" in job:
                apply_link = job["detected_extensions"].get("apply_link")

            # Option 2: Use the link field directly if it exists
            if not apply_link:
                apply_link = job.get("link")

            jobs.append({
                "title": job.get("title", "No title"),
                "company": job.get("company_name", "Not available"),
                "location": job.get("location", "Not available"),
                "snippet": job.get("description", "Not available"),
                "link": apply_link or "#"
            })

        return jobs

    except Exception as e:
        st.error(f"Scraping failed: {e}")
        return []

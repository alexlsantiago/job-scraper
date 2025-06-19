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
            # Prefer apply_link if available, otherwise fallback to 'link'
            apply_link = job.get("detected_extensions", {}).get("apply_link") or job.get("link")
            jobs.append({
                "title": job.get("title", "No title"),
                "company": job.get("company_name", "N/A"),
                "location": job.get("location", "N/A"),
                "snippet": job.get("description", "No summary available"),
                "link": apply_link
            })

        return jobs
    except Exception as e:
        st.error(f"Scraping failed: {e}")
        return []

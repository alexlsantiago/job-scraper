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
            job_data = {
                "title": job.get("title"),
                "company": job.get("company_name") or job.get("company"),
                "location": job.get("location"),
                "snippet": job.get("description") or job.get("snippet"),
                "link": (
                    job.get("detected_extensions", {}).get("link") or
                    (job.get("related_links")[0]["link"] if job.get("related_links") else None) or
                    job.get("link")
                )
            }
            jobs.append(job_data)

        return jobs

    except Exception as e:
        st.error(f"Scraping failed: {e}")
        return []

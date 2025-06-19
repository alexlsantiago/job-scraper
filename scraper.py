import requests
import streamlit as st
import urllib.parse

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
            title = job.get("title", "Unknown")
            company = job.get("company_name") or job.get("company") or "Unknown"
            location = job.get("location") or "Unknown"
            description = job.get("description") or job.get("snippet") or "No description available"

            # Try to get direct apply link or fallback to job link
            apply_link = job.get("apply_link") or job.get("link")

            # If no apply or job link, fallback to Google search link for the job
            if not apply_link:
                search_query = f"{title} {company} {location}".strip()
                encoded_query = urllib.parse.quote_plus(search_query)
                apply_link = f"https://www.google.com/search?q={encoded_query}"

            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "snippet": description,
                "link": apply_link
            })

        return jobs

    except Exception as e:
        st.error(f"Scraping failed: {e}")
        return []

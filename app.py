import streamlit as st
import os
import json
import zipfile
import requests
from datetime import datetime
from io import BytesIO

# === Direct SerpAPI request helper ===
def get_google_jobs_results(query, api_key, location="United States", hl="en", gl="us"):
    params = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "hl": hl,
        "gl": gl,
        "api_key": api_key,
    }
    response = requests.get("https://serpapi.com/search", params=params)
    response.raise_for_status()
    return response.json()

# === Streamlit UI ===
st.title("AI Job Scraper")

API_KEY = st.secrets.get("SERPAPI_KEY") or os.getenv("SERPAPI_KEY")

if not API_KEY:
    st.error("No SERPAPI_KEY found in Streamlit secrets or environment variables.")
    st.stop()

job_title = st.text_input("Job title", placeholder="e.g., Software Engineer Intern")
location = st.text_input("Location", placeholder="e.g., New York, United States")

if st.button("Scrape Jobs"):
    if not job_title:
        st.warning("Please enter a job title.")
    else:
        with st.spinner("Scraping job listings..."):
            try:
                results = get_google_jobs_results(job_title, API_KEY, location)
                jobs = results.get("jobs_results", [])
                if not jobs:
                    st.info("No jobs found.")
                else:
                    # Save to JSON in memory
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"jobs_{job_title}_{location}_{timestamp}.json".replace(" ", "_")
                    job_data = json.dumps(jobs, indent=2)

                    # Create a zip file in memory
                    zip_buffer = BytesIO()
                    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                        zip_file.writestr(filename, job_data)

                    st.success(f"Found {len(jobs)} jobs.")
                    st.download_button(
                        label="Download Results as ZIP",
                        data=zip_buffer.getvalue(),
                        file_name=f"{filename.replace('.json', '')}.zip",
                        mime="application/zip"
                    )

            except Exception as e:
                st.error(f"An error occurred: {e}")

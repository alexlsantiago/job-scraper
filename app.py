import streamlit as st
import pandas as pd
import zipfile
import io
from scraper import scrape_jobs

st.set_page_config(page_title="Job Scraper AI", layout="centered")

st.title("🧠 Job Scraper AI")
st.markdown("Search and download job listings from Google Jobs.")

query = st.text_input("🔍 Job title or keywords", placeholder="e.g. Python developer")
location = st.text_input("📍 Location", placeholder="e.g. New York or remote")

if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a job query.")
    else:
        with st.spinner("Scraping jobs..."):
            jobs = scrape_jobs(query, location)

        if not jobs:
            st.error("No jobs found.")
        else:
            st.success(f"Found {len(jobs)} jobs")

            # Show jobs on screen
            for job in jobs:
                st.markdown(f"### [{job.get('title')}]({job.get('link')})")
                st.markdown(f"**Company:** {job.get('company', 'N/A')}")
                st.markdown(f"**Location:** {job.get('location', 'N/A')}")
                st.markdown(f"**Summary:** {job.get('snippet', 'No summary available')}  ")
                st.markdown("---")

            # Export as CSV + ZIP
            df = pd.DataFrame(jobs)
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.writestr("jobs.csv", df.to_csv(index=False))
            buffer.seek(0)

            st.download_button(
                label="⬇️ Download Jobs as ZIP",
                data=buffer,
                file_name="job_listings.zip",
                mime="application/zip"
            )

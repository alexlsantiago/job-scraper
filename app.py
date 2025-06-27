import streamlit as st
import pandas as pd
import zipfile
import io
from scraper import scrape_jobs

st.set_page_config(page_title="Job Scraper AI", layout="centered")

st.markdown("""
    <div style='font-size: 2.5rem; font-weight: bold; margin-bottom: 0.5em;'>Job Scraper AI</div>
""", unsafe_allow_html=True)
st.markdown("Search and download job listings from Google Jobs.")

query = st.text_input("Job title or keywords", placeholder="e.g. Software Engineering Intern 2026")
location = st.text_input("Location", placeholder="e.g. New York or Austin, TX")

if "jobs" not in st.session_state:
    st.session_state.jobs = []

if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a job query.")
    else:
        with st.spinner("Scraping jobs..."):
            jobs = scrape_jobs(query, location)

        if not jobs:
            st.error("No jobs found.")
        else:
            st.session_state.jobs = jobs
            st.success(f"Found {len(jobs)} jobs")

# If there are jobs in session_state, show the download button and job listings
if st.session_state.jobs:
    df = pd.DataFrame(st.session_state.jobs)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("jobs.csv", df.to_csv(index=False))
    buffer.seek(0)

    st.download_button(
        label="Download Jobs as ZIP",
        data=buffer,
        file_name="job_listings.zip",
        mime="application/zip"
    )

    # Show jobs
    for job in st.session_state.jobs:
        title = job.get("title", "Untitled")
        link = job.get("external_link", job.get("link", "#"))
        company = job.get("company", "N/A")
        location = job.get("location", "N/A")
        summary = job.get("snippet", "No summary available")

        st.markdown(f"### [{title}]({link})")
        st.markdown(f"**Company:** {company}")
        st.markdown(f"**Location:** {location}")
        st.markdown(f"**Summary:** {summary}")
        st.markdown("---")

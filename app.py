import streamlit as st
from scraper import scrape_jobs

st.set_page_config(page_title="Job Scraper AI", layout="centered")

st.title("🔍 Job Scraper AI")
st.markdown("Search for jobs using live Google results.")

query = st.text_input("Enter job search query", placeholder="e.g. Python developer remote")

if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a valid job query.")
    else:
        with st.spinner("Scraping jobs..."):
            jobs = scrape_jobs(query)

        if not jobs:
            st.error("No jobs found.")
        else:
            st.success(f"Found {len(jobs)} jobs")
            for job in jobs:
                st.markdown(f"### [{job.get('title')}]({job.get('link')})")
                st.markdown(f"**Company:** {job.get('company', 'N/A')}")
                st.markdown(f"**Location:** {job.get('location', 'N/A')}")
                st.markdown(f"**Summary:** {job.get('snippet', 'No summary available')}  ")
                st.markdown("---")

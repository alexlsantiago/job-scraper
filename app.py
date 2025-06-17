import streamlit as st
import os
import zipfile
import re
import streamlit as st
from serpapi.google_search import GoogleSearch



API_KEY = st.secrets.get("SERPAPI_KEY")

if not API_KEY:
    st.error("❌ SERPAPI_KEY not found. Add it in Streamlit secrets.")
    st.stop()

# --- Streamlit Config + Matching Dark Theme ---
st.set_page_config(page_title="Job Finder", layout="centered")

# Custom dark theme styles with white preview text and no gray boxes
st.markdown(f"""
    <style>
            
        input::placeholder,
        textarea::placeholder {{
            color: #bbbbbb !important; 
            opacity: .55 !important;     
        }}
        html, body, .stApp {{
            background-color: #0e1117 !important;
            color: #fafafa !important;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #fafafa !important;
        }}
        h1 a, h2 a, h3 a, h4 a {{
            display: none !important;
        }}

        .stTextInput > div > div > input,
        .stTextArea textarea,
        .stSelectbox div div div,
        .stFileUploader > div > div,
        .stDownloadButton button,
        .stButton button {{
            background-color: #262730 !important;
            color: #fafafa !important;
            border-radius: 5px;
            border: none;
        }}
        .stMarkdown {{
            color: #fafafa !important;
        }}
        .stButton button, .stDownloadButton button {{
            background-color: #4f8bf9 !important;
            color: white !important;
            padding: 0.5rem 1rem;
        }}
        .stSlider > div,
        label, .stTextInput label, .stTextArea label {{
            color: #fafafa !important;
        }}
        header, footer {{
            background: transparent !important;
        }}
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='white-space: nowrap;'>AI-Powered Job Finder</h1>
""", unsafe_allow_html=True)


# --- Scraping Logic ---
def scrape_jobs(query, location, max_jobs):
    params = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "hl": "en",
        "gl": "us",
        "api_key": API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    jobs_raw = results.get("jobs_results", [])
    jobs = []

    for job in jobs_raw[:max_jobs]:
        jobs.append({
            "title": job.get("title", "No Title"),
            "company": job.get("company_name", "Unknown Company"),
            "link": job.get("apply_options", [{}])[0].get("link") or job.get("via", ""),
            "description": job.get("description", "No description found.")
        })

    return jobs

def export_jobs_to_zip(jobs, zip_path="jobs.zip"):
    with zipfile.ZipFile(zip_path, "w") as z:
        for i, job in enumerate(jobs):
            safe_title = re.sub(r'[^a-zA-Z0-9]+', '_', job['title'])[:40]
            filename = f"{safe_title}_{i}.txt"
            content = f"{job['title']} at {job['company']}\n{job['link']}\n\n{job['description']}"
            z.writestr(filename, content)

# --- UI Form ---
with st.form("scrape_form"):
    query = st.text_input("Search Jobs For", placeholder="e.g. 'Software Engineering Intern 2026'")
    location = st.text_input("Location", placeholder="e.g. 'Austin, TX'")
    max_jobs = st.slider("Number of jobs", min_value=1, max_value=10, value=5)
    submitted = st.form_submit_button("🔍 Scrape Jobs")

# --- Submission Handling ---
if submitted:
    if not API_KEY:
        st.error("❌ SERPAPI_KEY not found in environment. Please set it in a .env file.")
    else:
        with st.spinner("Scraping job listings..."):
            jobs = scrape_jobs(query, location, max_jobs)
        if not jobs:
            st.warning("⚠️ No jobs found. Try a different query or location.")
        else:
            st.success(f"✅ Found {len(jobs)} jobs!")
            st.session_state["jobs"] = jobs  # store jobs to persist across interactions
            export_jobs_to_zip(jobs, "jobs.zip")

# --- Display Jobs Preview & Download ---
if "jobs" in st.session_state:
    jobs = st.session_state["jobs"]

    st.download_button(
        label="📥 Download Jobs ZIP",
        data=open("jobs.zip", "rb").read(),
        file_name="jobs.zip",
        mime="application/zip"
    )

    st.subheader("📄 Preview")
    for job in jobs:
        st.markdown(f"<h4 style='color: #fafafa;'>{job['title']}</h4>", unsafe_allow_html=True)
        st.markdown(f"<i style='color: #cccccc;'>{job['company']}</i>", unsafe_allow_html=True)
        st.markdown(f"<a href='{job['link']}' style='color: #4f8bf9;' target='_blank'>Apply Here</a>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #fafafa;'>{job['description'][:300]}...</p>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

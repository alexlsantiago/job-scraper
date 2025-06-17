import os
import zipfile
import argparse
import re
from serpapi import GoogleSearch
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("SERPAPI_KEY")

def scrape_serpapi_jobs(query, location, max_jobs=5):
    jobs = []
    start = 0

    while len(jobs) < max_jobs:
        params = {
            "engine": "google_jobs",
            "q": query,
            "location": location,
            "hl": "en",
            "gl": "us",
            "api_key": API_KEY,
            "start": start
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        jobs_raw = results.get("jobs_results", [])

        if not jobs_raw:
            break

        for job in jobs_raw:
            jobs.append({
                "title": job.get("title", "No Title"),
                "company": job.get("company_name", "Unknown Company"),
                "description": job.get("description", "No description found."),
                "link": job.get("apply_options", [{}])[0].get("link") or job.get("via", "")
            })

            if len(jobs) >= max_jobs:
                break

        start += 10

    return jobs

def export_jobs_to_zip(jobs, zip_path="jobs.zip"):
    with zipfile.ZipFile(zip_path, "w") as z:
        for i, job in enumerate(jobs):
            safe_title = re.sub(r'[^a-zA-Z0-9]+', '_', job['title'])[:40]
            filename = f"{safe_title}_{i}.txt"
            content = f"{job['title']} at {job['company']}\n{job['link']}\n\n{job['description']}"
            z.writestr(filename, content)
    print(f"✅ Saved {len(jobs)} jobs to {zip_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape job descriptions using SerpAPI.")
    parser.add_argument("--query", type=str, required=True, help="Search term, e.g., 'data scientist'")
    parser.add_argument("--location", type=str, default="Remote", help="Job location")
    parser.add_argument("--max", type=int, default=5, help="Number of jobs to fetch")
    parser.add_argument("--output", type=str, default="jobs.zip", help="Output ZIP filename")

    args = parser.parse_args()

    jobs = scrape_serpapi_jobs(args.query, args.location, args.max)

    if not jobs:
        print("⚠️ No jobs found. Try a broader query or location.")
    else:
        export_jobs_to_zip(jobs, args.output)

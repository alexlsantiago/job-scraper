# scraper.py
import os
import json
import argparse
import requests
from datetime import datetime

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

def main():
    parser = argparse.ArgumentParser(description="Scrape job listings using SerpAPI.")
    parser.add_argument("query", help="Search query (e.g., Software Engineer Intern)")
    parser.add_argument("--location", default="United States", help="Location (default: US)")
    parser.add_argument("--output", default=None, help="Output JSON filename")
    args = parser.parse_args()

    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        raise RuntimeError("SERPAPI_KEY environment variable not set.")

    print(f"Searching for: '{args.query}' in '{args.location}'")

    data = get_google_jobs_results(args.query, api_key, args.location)
    jobs = data.get("jobs_results", [])

    if not jobs:
        print("No jobs found.")
        return

    filename = args.output or f"jobs_{args.query}_{args.location}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filename = filename.replace(" ", "_")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)

    print(f"Saved {len(jobs)} job results to {filename}")

if __name__ == "__main__":
    main()

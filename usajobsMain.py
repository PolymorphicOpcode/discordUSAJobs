import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
KEY = os.getenv("USAJOBS_API_KEY")
EMAIL = os.getenv("USAJOBS_API_EMAIL")

def get_credentials():
    """Retrieve credentials from environment variables or prompt the user."""
    email = EMAIL
    api_key = KEY

    if not email or not api_key:
        if not email:
            email = input("Enter your USAJobs Email: ").strip()
        if not api_key:
            api_key = input("Enter your USAJobs API Key: ").strip()

    return email, api_key

def fetch_job_listings(email, api_key):
    """Fetch job listings from the USAJobs API."""
    api_url = "https://data.usajobs.gov/api/search"

    # Set up headers
    headers = {
        "User-Agent": email,
        "Authorization-Key": api_key
    }

    # Query parameters
    params = {
        "HiringPath": "student",
        "SortField": "opendate",
        "SortDirection": "desc",
        "ResultsPerPage": "100",
        "DatePosted": "1"  # Jobs posted within the last week
    }

    # Perform the API request
    response = requests.get(api_url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

    return response.json()

def format_jobs(api_response):
    """Format job listings for output."""
    jobs = api_response.get("SearchResult", {}).get("SearchResultItems", [])

    output_lines = []
    for item in jobs:
        job = item.get("MatchedObjectDescriptor", {})
        line = f"{job.get('PublicationStartDate', 'N/A')}, {job.get('PositionTitle', 'N/A')}, {job.get('OrganizationName', 'N/A')}, {job.get('ApplicationCloseDate', 'N/A')}, {job.get('PositionURI', 'N/A')}"
        output_lines.append(line)

    return "\n".join(output_lines)

def main():
    try:
        email, api_key = get_credentials()
        api_response = fetch_job_listings(email, api_key)
        formatted_output = format_jobs(api_response)
        print(formatted_output)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
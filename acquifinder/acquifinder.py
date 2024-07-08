from apify_client import ApifyClient
from re import findall
import os
from dotenv import load_dotenv
import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load environment variables
load_dotenv()

# Initialize Apify client
apify_API_KEY = os.getenv("Apify_API_KEY")
client = ApifyClient(apify_API_KEY)

def fetch_google_search_results(query):
    """
    Fetch organic search results from Google using Apify Google Search Scraper.
    Returns a list of titles from the organic results.
    """
    try:
        run_input = {
            "queries": query,
            "resultsPerPage": 100,
            "maxPagesPerQuery": 1,
        }
        run = client.actor("apify/google-search-scraper").call(run_input=run_input)

        titles = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            for res in item["organicResults"]:
                titles.append(res["title"])

        return titles

    except Exception as e:
        print(f"Error fetching Google search results: {e}")
        return []

def find_acquisitions(company_name):
    """
    Find acquisitions related to the given company name using Google search results.
    Returns a list of acquisitions found.
    """
    try:
        query = f'site:crunchbase.com "{company_name} acquires"'
        titles = fetch_google_search_results(query)

        pattern = rf"{company_name} acquires ([^-]+)"
        acquisitions = findall(pattern, str(titles))

        return acquisitions

    except Exception as e:
        print(f"Error finding acquisitions: {e}")
        return []

def fetch_acquisitions(company_name, sleep_time=0, verbose=False, num_threads=1):
    """
    Fetch acquisitions for the given company name from multiple sources.
    Returns a list of acquisitions found.
    """
    acquisitions = []

    def fetch_acquisitions_threaded(company_name):
        return find_acquisitions(company_name)

    # Use ThreadPoolExecutor for concurrent fetching if num_threads > 1
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_company = {executor.submit(fetch_acquisitions_threaded, company): company for company in [company_name]}
        for future in as_completed(future_to_company):
            company = future_to_company[future]
            try:
                acquisitions.extend(future.result())
            except Exception as e:
                print(f"Failed to fetch acquisitions for {company}: {e}")

    return acquisitions

def main(company_name, sleep_time=0, verbose=False, num_threads=1):
    try:
        if verbose:
            print(f"Fetching acquisitions for {company_name}...")

        acquisitions = fetch_acquisitions(company_name, sleep_time, verbose, num_threads)
        
        if acquisitions:
            print(f"Acquisitions by {company_name}:")
            for acquisition in acquisitions:
                print(acquisition)
        else:
            print(f"No acquisitions found for {company_name}.")

    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch acquisitions data for a company.')
    parser.add_argument('company_name', type=str, help='Name of the company to search acquisitions for.')
    parser.add_argument('--sleep', type=float, default=0, help='Delay in seconds between requests.')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output.')
    parser.add_argument('--threads', type=int, default=1, help='Number of threads for concurrent processing.')

    args = parser.parse_args()
    main(args.company_name, args.sleep, args.verbose, args.threads)

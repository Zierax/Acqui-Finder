# Acquisitions Reconnaissance Tool

A Python script for fetching acquisitions data related to companies from various sources, utilizing the Apify Google Search Scraper API.

## Features

- Fetch acquisitions data from Crunchbase using Google search queries.
- Support for concurrent processing with adjustable thread count.
- Customizable delay between requests.
- Verbose mode for detailed output.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Zierax/Acqui-Finder.git
   cd Acqui-Finder
   ```
Install dependencies:

```
pip install -r requirements.txt
```
Set up environment variables:

Create a .env file in the root directory with your Apify API key:

```makefile
Apify_API_KEY=your_apify_api_key_here
```

import requests
import time
from pprint import pprint

class GoogleSearchAPI:
    def __init__(self, cse_id, google_console_api_key):
        self.cse_id = cse_id
        self.api_key = google_console_api_key
        self.url = "https://www.googleapis.com/customsearch/v1"
        self.max_retries = 5
        self.backoff_factor = 1

    def search_linkedin_by_email(self, email):
        query = f"{email} site:linkedin.com"
        params = {
            'q': query,
            'cx': self.cse_id,
            'key': self.api_key,
            'num': 2
        }
        
        for attempt in range(self.max_retries):
            response = requests.get(self.url, params=params)
            if response.status_code == 200:
                return self._extract_linkedin_urls(response.json())
            elif response.status_code == 429:
                self._handle_rate_limit(attempt)
            elif response.status_code == 400:
                print("Bad request. Please check your API key and parameters.")
                return None
            else:
                print(f"Error: {response.status_code}")
                return None
        print("Max retries reached. Returning None.")
        return None

    def _extract_linkedin_urls(self, data):
        linkedin_urls = [item.get('link') for item in data.get('items', []) if 'linkedin.com/in/' in item.get('link', '')]
        return linkedin_urls[0] if linkedin_urls else None

    def _handle_rate_limit(self, attempt):
        wait_time = self.backoff_factor * (2 ** attempt)
        print(f"Rate limit exceeded. Waiting for {wait_time} seconds before retrying...")
        time.sleep(wait_time)

# Example usage:
# google_search_api = GoogleSearchAPI(cse_id="9526871902fac4c02", api_key="AIzaSyDW1oEs7ATWYIL_To8Wh5-iIiq2EFa5z1I")
# linkedin_url = google_search_api.search_linkedin_by_email("example@example.com")
# print(linkedin_url)
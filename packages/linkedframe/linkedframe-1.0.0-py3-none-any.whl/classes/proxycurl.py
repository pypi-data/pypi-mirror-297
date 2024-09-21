import time
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import multiprocessing
import pandas as pd
import os

class LinkedInDataProcessor:
    def __init__(self, open_ai_client, api_key_proxycurl):
        self.open_ai_client = open_ai_client
        self.api_key_proxycurl = api_key_proxycurl
        if not self.api_key_proxycurl:
            raise ValueError("API key for ProxyCurl not provided")

    def get_linkedin_data_from_url(self, linkedin_url) -> dict | None:
        headers = {"Authorization": f"Bearer {self.api_key_proxycurl}"}
        endpoint = os.getenv('PROXYCURL_ENDPOINT', "https://nubela.co/proxycurl/api/v2/linkedin")
        query_params = {
            "linkedin_profile_url": linkedin_url,
            "skills": "include",
        }
        try:
            response = requests.get(endpoint, params=query_params, headers=headers)
            response.raise_for_status()
            data = response.json()
            data["linkedin_url"] = linkedin_url
            return data
        except requests.RequestException as e:
            print(f"Error fetching LinkedIn data: {e}")
            return None

    def enrich_linkedin_data(self, linkedin_data):
        if linkedin_data:
            linkedin_data["educational_level"] = self.open_ai_client.get_education_level(linkedin_data.get("education", ""))
            linkedin_data["work_field"] = self.open_ai_client.get_work_fields(linkedin_data.get("experiences", ""))
            linkedin_data["profile_language"] = self.open_ai_client.get_language(linkedin_data.get("summary", ""))
        return linkedin_data or {}

    def process_row(self, row):
        linkedin_data = row.get('linkedin_data', {})
        linkedin_data = self.enrich_linkedin_data(linkedin_data) if isinstance(linkedin_data, dict) else {}
        keys_to_update = [
            'educational_level', 'work_field', 'profile_language', 'public_identifier', 'profile_pic_url',
            'background_cover_image_url', 'first_name', 'last_name', 'full_name', 'occupation', 'headline',
            'summary', 'country', 'country_full_name', 'city', 'state', 'languages', 'skills', 'connections'
        ]
        row.update({key: linkedin_data.get(key) for key in keys_to_update})
        return row

    def process_linkedin_data(self, df):
        records = df.to_dict('records')
        num_cores = multiprocessing.cpu_count()
        
        def fetch_linkedin_data(row):
            max_retries = 3
            for _ in range(max_retries):
                try:
                    return self.get_linkedin_data_from_url(row['linkedin_url'])
                except requests.exceptions.ChunkedEncodingError:
                    time.sleep(1) 
            return None  
        
        with ThreadPoolExecutor(max_workers=num_cores) as executor:
            linkedin_data_list = list(tqdm(executor.map(fetch_linkedin_data, records), total=len(records), desc="Fetching LinkedIn data"))
        
        for record, data in zip(records, linkedin_data_list):
            if data is not None:
                record['linkedin_data'] = data
        
        with ThreadPoolExecutor(max_workers=num_cores) as executor:
            processed_records = list(tqdm(executor.map(self.process_row, records), total=len(records), desc="Processing LinkedIn data"))
        
        df = pd.DataFrame(processed_records)
        df.drop(columns=['linkedin_url'], inplace=True, errors='ignore')
        return df
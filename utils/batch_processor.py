import time
from typing import List, Dict
from urllib.parse import urlencode
from config.constants import *

class BatchProcessor:
    def __init__(self):
        self.request_timestamps = []
        self.last_request_time = 0

    def check_rate_limits(self):
        current_time = time.time()
        # Clean old timestamps
        self.request_timestamps = [
            ts for ts in self.request_timestamps 
            if current_time - ts < 300  # 5 minutes
        ]
        
        # Check limits
        if len(self.request_timestamps) >= RATE_LIMIT_PER_5_MINUTES:
            sleep_time = 300 - (current_time - self.request_timestamps[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
                return self.check_rate_limits()
                
        minute_requests = len([
            ts for ts in self.request_timestamps 
            if current_time - ts < 60
        ])
        if minute_requests >= RATE_LIMIT_PER_MINUTE:
            sleep_time = 60 - (current_time - self.request_timestamps[-RATE_LIMIT_PER_MINUTE])
            if sleep_time > 0:
                time.sleep(sleep_time)
                return self.check_rate_limits()

    def create_batched_url(self, items: List[str], locations: List[str]) -> str:
        base_url = f"{BASE_URL}"
        items_param = ",".join(items)
        locations_param = ",".join(locations)
        params = {
            "locations": locations_param,
            "qualities": "1"
        }
        url = f"{base_url}{items_param}.json?{urlencode(params)}"
        
        if len(url) > MAX_URL_LENGTH:
            raise ValueError(f"URL length ({len(url)}) exceeds maximum ({MAX_URL_LENGTH})")
        
        return url
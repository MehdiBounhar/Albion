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
            ts for ts in self.request_timestamps if current_time - ts < 300  # 5 minutes
        ]

        # Check limits
        if len(self.request_timestamps) >= RATE_LIMIT_PER_5_MINUTES:
            sleep_time = 300 - (current_time - self.request_timestamps[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
                return self.check_rate_limits()

        minute_requests = len(
            [ts for ts in self.request_timestamps if current_time - ts < 60]
        )
        if minute_requests >= RATE_LIMIT_PER_MINUTE:
            sleep_time = 60 - (
                current_time - self.request_timestamps[-RATE_LIMIT_PER_MINUTE]
            )
            if sleep_time > 0:
                time.sleep(sleep_time)
                return self.check_rate_limits()

    def create_batched_url(self, items: List[str], locations: List[str]) -> List[str]:
        """
        Creates batched URLs ensuring each URL is within length limit
        Returns a list of valid URLs
        """
        base_url = BASE_URL
        locations_param = ",".join(locations)
        base_params = {"locations": locations_param, "qualities": "1"}
        base_query = urlencode(base_params)
        base_length = len(base_url) + len(".json?") + len(base_query)

        urls = []
        current_batch = []
        current_url_length = base_length

        for item in items:
            # Calculate length with new item
            separator = "," if current_batch else ""
            new_item_length = len(separator) + len(item)
            test_length = current_url_length + new_item_length

            if test_length <= MAX_URL_LENGTH:
                # Add item to current batch
                current_batch.append(item)
                current_url_length = test_length
            else:
                # Current batch is full, create URL and start new batch
                if current_batch:
                    items_param = ",".join(current_batch)
                    url = f"{base_url}{items_param}.json?{base_query}"
                    urls.append(url)

                # Start new batch with current item
                current_batch = [item]
                current_url_length = base_length + len(item)

        # Add remaining items
        if current_batch:
            items_param = ",".join(current_batch)
            url = f"{base_url}{items_param}.json?{base_query}"
            urls.append(url)

        return urls

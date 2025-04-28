import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import pandas as pd
import time
import streamlit as st
from typing import Optional, List
from .batch_processor import BatchProcessor
from config.constants import BATCH_SIZE, CITIES


class DataFetcher:
    def __init__(self):
        self.batch_processor = BatchProcessor()
        self.session = self.create_session()

    def create_session(self):
        """Create a requests session with retry strategy"""
        session = requests.Session()
        retry_strategy = Retry(
            total=5,  # number of retries
            backoff_factor=1,  # delay between retries
            status_forcelist=[429, 500, 502, 503, 504],  # status codes to retry on
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    @staticmethod
    def construct_item_id(resource: str, tier: int, enchantment: int) -> str:
        if enchantment == 0:
            return f"T{tier}_{resource}"
        return f"T{tier}_{resource}_LEVEL{enchantment}@{enchantment}"

    @staticmethod
    def fetch_prices(url: str) -> pd.DataFrame:
        response = requests.get(url)
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            if (
                "sell_price_max_date"
                or "buy_price_min_date"
                or "buy_price_max_date" in df.columns
            ):
                df = df[df["sell_price_max_date"] != "0001-01-01T00:00:00"]
                df = df[df["sell_price_min_date"] != "0001-01-01T00:00:00"]
                df = df[df["buy_price_min_date"] != "0001-01-01T00:00:00"]
                df = df[df["buy_price_max_date"] != "0001-01-01T00:00:00"]
            # Save the corrected DataFrame to a CSV file
            df.to_csv("corrected_data.csv", index=False)
            return df
        print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
        return pd.DataFrame()

    @staticmethod
    def fetch_artifact_prices(url: str) -> pd.DataFrame:
        """Fetch prices with lenient date filtering specifically for artifact foundry."""
        response = requests.get(url)
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            if not df.empty:
                # Only filter out rows where all dates are invalid
                date_columns = [col for col in df.columns if col.endswith("_date")]
                if date_columns:
                    # Create a mask for valid rows (at least one valid date)
                    valid_rows = pd.Series(False, index=df.index)
                    for col in date_columns:
                        valid_rows |= df[col] != "0001-01-01T00:00:00"
                    df = df[valid_rows]
            return df
        print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
        return pd.DataFrame()

    @staticmethod
    def fetch_prices_for_black_market(url: str) -> Optional[pd.DataFrame]:
        response = requests.get(url)
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            if (
                "sell_price_max_date"
                or "buy_price_min_date"
                or "buy_price_max_date" in df.columns
            ):
                df = df[df["sell_price_max_date"] != "0001-01-01T00:00:00"]
                df = df[df["buy_price_min_date"] != "0001-01-01T00:00:00"]
                df = df[df["buy_price_max_date"] != "0001-01-01T00:00:00"]
                df = df[df["sell_price_min_date"] != "0001-01-01T00:00:00"]
            return df
        print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
        return None

    def fetch_bulk_prices(self, items: List[str]) -> pd.DataFrame:
        """Fetch prices for multiple items in batches"""
        all_data = []

        try:
            # Get batched URLs
            urls = self.batch_processor.create_batched_url(items, CITIES)

            # Process each URL
            for idx, url in enumerate(urls):
                self.batch_processor.check_rate_limits()

                try:
                    response = self.session.get(url)
                    if response.status_code == 200:
                        data = response.json()
                        all_data.extend(data)
                        self.batch_processor.request_timestamps.append(time.time())
                    else:
                        st.warning(
                            f"Batch {idx+1} failed with status code: {response.status_code}"
                        )
                except Exception as e:
                    st.warning(f"Error fetching batch {idx+1}: {str(e)}")
                    continue

            return pd.DataFrame(all_data) if all_data else pd.DataFrame()

        except Exception as e:
            st.error(f"Failed to fetch prices: {str(e)}")
            return pd.DataFrame()

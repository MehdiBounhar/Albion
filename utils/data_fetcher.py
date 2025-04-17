import requests
import pandas as pd
import streamlit as st
from typing import Optional, List


class DataFetcher:
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
            if "sell_price_max_date" or "buy_price_min_date" or "buy_price_max_date" in df.columns:
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
    def fetch_prices_for_black_market(
        url: str
    ) -> Optional[pd.DataFrame]:
        response = requests.get(url)
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            if "sell_price_max_date" or "buy_price_min_date" or "buy_price_max_date" in df.columns:
                df = df[df["sell_price_max_date"] != "0001-01-01T00:00:00"]
                df = df[df["buy_price_min_date"] != "0001-01-01T00:00:00"]
                df = df[df["buy_price_max_date"] != "0001-01-01T00:00:00"]
                df = df[df["sell_price_min_date"] != "0001-01-01T00:00:00"]
            return df
        print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
        return None

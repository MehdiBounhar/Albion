import pandas as pd
import streamlit as st
import requests
import json
from typing import Dict, List, Optional
from utils.data_fetcher import DataFetcher
from config.constants import RESOURCE_TYPES, TIERS, ENCHANTMENTS, CITIES, BASE_URL


class MarketAnalyzer:
    @staticmethod
    def find_opportunities(df: pd.DataFrame) -> Optional[Dict]:
        if df.empty or len(df) < 2:
            return None

        df = df[df["sell_price_min"] > 0]
        if df.empty:
            return None

        best_buy = df.sort_values("sell_price_min").head(1)
        best_sell = df.sort_values("sell_price_min", ascending=False).head(1)

        if best_buy.empty or best_sell.empty:
            return None

        buy_price = best_buy.iloc[0]["sell_price_min"]
        sell_price = best_sell.iloc[0]["sell_price_min"]

        if buy_price == 0 or sell_price == 0 or sell_price <= buy_price:
            return None

        return {
            "buy_city": best_buy.iloc[0]["city"],
            "buy_price": buy_price,
            "buy_price_date": best_buy.iloc[0]["sell_price_min_date"],
            "sell_city": best_sell.iloc[0]["city"],
            "sell_price": sell_price,
            "sell_price_date": best_sell.iloc[0]["sell_price_min_date"],
            "profit": sell_price - buy_price,
        }

    @staticmethod
    def run_market_analysis(
        analysis_type: str = "Arbitrage Opportunities",
    ) -> List[Dict]:
        if analysis_type == "Arbitrage Opportunities":
            return MarketAnalyzer._run_arbitrage_analysis()
        elif analysis_type == "Black Market":
            return MarketAnalyzer._run_black_market_analysis()
        elif analysis_type == "Price Comparison":
            return st.error("Price Comparison analysis is not implemented yet.")
        return []

    @staticmethod
    def _run_arbitrage_analysis() -> List[Dict]:
        all_item_ids = [
            DataFetcher.construct_item_id(res, t, e)
            for res in RESOURCE_TYPES
            for t in TIERS
            for e in ENCHANTMENTS
        ]
        with open("all_item_ids.txt", "w") as file:
            file.write("\n".join(all_item_ids))
        opportunities = []
        progress_bar = st.progress(0)
        total_batches = (len(all_item_ids) + 49) // 50  # Round up division

        for batch_num, i in enumerate(range(0, len(all_item_ids), 50)):
            batch_ids = all_item_ids[i : i + 50]
            url = f"{BASE_URL}{','.join(batch_ids)}.json?locations={','.join(CITIES)}&qualities=1"

            response = requests.get(url)
            if response.status_code != 200:
                continue

            df_all = pd.DataFrame(response.json())
            df_all = df_all[df_all["sell_price_min"] > 0]

            for item in df_all["item_id"].unique():
                subset = df_all[df_all["item_id"] == item]
                opportunity = MarketAnalyzer.find_opportunities(subset)
                if opportunity:
                    opportunity["item_id"] = item
                    opportunities.append(opportunity)

            progress_bar.progress((batch_num + 1) / total_batches)

        return opportunities

    @staticmethod
    def _run_black_market_analysis() -> List[Dict]:
        # Load items from JSON
        try:
            with open("config/items_cleaned.json", "r", encoding="utf-8") as f:
                items_data = json.load(f)
        except FileNotFoundError:
            st.error(
                "Items database not found. Please ensure items_cleaned.json exists."
            )
            return []

        opportunities = []
        progress_bar = st.progress(0)

        # Get unique item names
        unique_items = [item["UniqueName"] for item in items_data]

        # Initialize DataFetcher
        data_fetcher = DataFetcher()

        with st.spinner("Fetching Black Market data in batches..."):
            # Fetch all data using bulk prices
            df_all = data_fetcher.fetch_bulk_prices(unique_items)

            if df_all.empty:
                st.warning("No data available from the market")
                return []

            # Process each item
            total_items = len(df_all["item_id"].unique())
            for idx, item in enumerate(df_all["item_id"].unique()):
                item_df = df_all[df_all["item_id"] == item]

                # Get Black Market data
                bm_data = item_df[item_df["city"] == "Black Market"]
                other_cities = item_df[item_df["city"] != "Black Market"]

                if not bm_data.empty and not other_cities.empty:
                    # Black Market buy price (what they pay)
                    bm_buy_price = bm_data.iloc[0]["buy_price_max"]

                    # Find best sell price in other cities
                    best_sell = other_cities.sort_values("sell_price_min").head(1)
                    market_price = best_sell.iloc[0]["sell_price_min"]

                    # Calculate profit
                    if bm_buy_price > market_price and market_price > 0:
                        opportunities.append(
                            {
                                "item_id": item,
                                "buy_city": best_sell.iloc[0]["city"],
                                "buy_price": market_price,
                                "buy_price_date": best_sell.iloc[0][
                                    "buy_price_min_date"
                                ],
                                "sell_city": "Black Market",
                                "sell_price": bm_buy_price,
                                "sell_price_date": bm_data.iloc[0][
                                    "buy_price_max_date"
                                ],
                                "profit": bm_buy_price - market_price,
                            }
                        )

                progress_bar.progress((idx + 1) / total_items)

        # Sort opportunities by profit
        opportunities.sort(key=lambda x: x["profit"], reverse=True)
        return opportunities

import streamlit as st
from config.constants import *
from utils.data_fetcher import DataFetcher
from analysis.market_analyzer import MarketAnalyzer
from components.ui import (
    display_market_prices,
    display_analysis_results,
    display_black_market_results,
)


def initialize_session_state():
    if "arbitrage_opportunities" not in st.session_state:
        st.session_state.arbitrage_opportunities = None
    if "black_market_opportunities" not in st.session_state:
        st.session_state.black_market_opportunities = None


def main():
    # Initialize session state
    initialize_session_state()

    st.set_page_config(page_title="Albion Resource Prices", layout="wide")
    st.title("📦 Albion Online Resource Price Dashboard")

    # Display Tabs
    tabs = st.tabs(
        ["📊 Market Overview", "💸 Resource Arbitrage", "🏴‍☠️ Black Market Flips"]
    )

    with tabs[0]:
        st.subheader("📈 Market Overview")
        # Item selector for market overview
        col1, col2, col3 = st.columns(3)
        with col1:
            resource = st.selectbox("Resource", RESOURCE_TYPES)
        with col2:
            tier = st.selectbox("Tier", TIERS)
        with col3:
            enchant = st.selectbox("Enchantment", ENCHANTMENTS)

        item_id = DataFetcher.construct_item_id(resource, tier, enchant)
        url = f"{BASE_URL}{item_id}.json?locations={','.join(CITIES)}&qualities=1"
        df = DataFetcher.fetch_prices(url)
        display_market_prices(df, item_id)

    with tabs[1]:
        st.subheader("💸 Resource Arbitrage Opportunities")
        if st.session_state.arbitrage_opportunities is None:
            with st.spinner("Running arbitrage analysis..."):
                opportunities = MarketAnalyzer.run_market_analysis(
                    "Arbitrage Opportunities"
                )
                st.session_state.arbitrage_opportunities = opportunities

        display_analysis_results(st.session_state.arbitrage_opportunities)
        if st.button("🔄 Refresh Arbitrage Analysis"):
            with st.spinner("Refreshing arbitrage analysis..."):
                opportunities = MarketAnalyzer.run_market_analysis(
                    "Arbitrage Opportunities"
                )
                st.session_state.arbitrage_opportunities = opportunities

    with tabs[2]:
        st.subheader("🏴‍☠️ Black Market Opportunities")
        if st.session_state.black_market_opportunities is None:
            with st.spinner("Running Black Market analysis..."):
                opportunities = MarketAnalyzer.run_market_analysis("Black Market")
                st.session_state.black_market_opportunities = opportunities

        display_black_market_results(st.session_state.black_market_opportunities)
        if st.button("🔄 Refresh Black Market Analysis"):
            with st.spinner("Refreshing Black Market analysis..."):
                opportunities = MarketAnalyzer.run_market_analysis("Black Market")
                st.session_state.black_market_opportunities = opportunities


if __name__ == "__main__":
    main()

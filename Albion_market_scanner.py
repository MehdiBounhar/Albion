import streamlit as st
from config.constants import *
from utils.data_fetcher import DataFetcher
from analysis.market_analyzer import MarketAnalyzer
from components.ui import display_market_prices, display_analysis_results


def initialize_session_state():
    if "analysis_type" not in st.session_state:
        st.session_state.analysis_type = "Arbitrage Opportunities"
    if "all_opportunities" not in st.session_state:
        st.session_state.all_opportunities = None


def main():
    # Initialize session state
    initialize_session_state()

    st.set_page_config(page_title="Albion Resource Prices", layout="wide")
    st.title("📦 Albion Online Resource Price Dashboard")

    # Process Data for single item view
    resource = st.sidebar.selectbox("Select Resource", RESOURCE_TYPES)
    tier = st.sidebar.selectbox("Select Tier", TIERS)
    enchant = st.sidebar.selectbox("Select Enchantment", ENCHANTMENTS)

    item_id = DataFetcher.construct_item_id(resource, tier, enchant)
    url = f"{BASE_URL}{item_id}.json?locations={','.join(CITIES)}&qualities=1"
    df = DataFetcher.fetch_prices(url)

    # Display Tabs
    tabs = st.tabs(["📊 Market Prices", "💸 Profitable Items"])

    with tabs[0]:
        display_market_prices(df, item_id)

    with tabs[1]:
        # Market Analysis Configuration
        st.sidebar.markdown("---")
        st.sidebar.header("🔍 Market Analysis")

        st.session_state.analysis_type = st.sidebar.radio(
            "Select Analysis Type",
            options=["Arbitrage Opportunities", "Black Market", "Price Comparison"],
        )

        # Add Analysis Button
        if st.sidebar.button("🔍 Run Market Analysis"):
            with st.spinner(f"Running {st.session_state.analysis_type} analysis..."):
                opportunities = MarketAnalyzer.run_market_analysis(
                    st.session_state.analysis_type
                )
                st.session_state.all_opportunities = opportunities

        # Display Analysis Results
        if st.session_state.all_opportunities is not None:
            st.subheader(f"📈 {st.session_state.analysis_type}")
            display_analysis_results(st.session_state.all_opportunities)
        else:
            st.info("Click 'Run Market Analysis' to discover profitable items.")


if __name__ == "__main__":
    main()

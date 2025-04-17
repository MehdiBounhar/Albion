import streamlit as st
import pandas as pd
from typing import Dict, List
from datetime import datetime, timezone


def get_hours_ago(timestamp_str: str) -> float:
    """Convert timestamp to hours ago and return hours as float"""
    # Parse timestamp and ensure it's UTC aware
    timestamp = pd.to_datetime(timestamp_str).tz_localize("UTC")
    # Get current time in UTC
    now = pd.to_datetime(datetime.now(timezone.utc))
    delta = now - timestamp
    return delta.total_seconds() / 3600


def style_time_cell(time_str: str) -> str:
    """Return CSS style based on how old the data is"""
    # Handle minute cases
    if "m ago" in time_str:
        return "color: #00FF00"  # Green for all minute-based times

    # Handle hour cases
    try:
        hours = float(time_str.split("h")[0])
        if hours <= 7:
            return "color: #00FF00"  # Green
        elif hours <= 16:
            return "color: #FFA500"  # Orange
        else:
            return "color: #FF0000"  # Red
    except:
        return ""


def format_time_ago(hours: float) -> str:
    """Format hours into a readable string"""
    if hours < 1:
        minutes = int(hours * 60)
        return f"{minutes} m ago"
    return f"{hours:.1f} h ago"


def display_market_prices(df: pd.DataFrame, item_id: str):
    st.subheader(f"📊 Market Prices for {item_id}")
    if df.empty:
        st.warning("No market data available.")
        return

    # Create a copy to avoid modifying the original dataframe
    display_df = df.copy()

    # Find all timestamp columns
    timestamp_columns = [col for col in df.columns if col.endswith("_date")]

    # Process each timestamp column
    for col in timestamp_columns:
        base_name = col.replace("_date", "")
        # Calculate hours ago for each timestamp
        display_df[f"{base_name}_age"] = df[col].apply(get_hours_ago)
        # Format the display string
        display_df[f"{base_name}_updated"] = display_df[f"{base_name}_age"].apply(
            format_time_ago
        )
        # Drop original and intermediate columns
        display_df = display_df.drop(columns=[col, f"{base_name}_age"])

    # Reorder columns
    price_columns = [
        "sell_price_min",
        "sell_price_max",
        "buy_price_min",
        "buy_price_max",
    ]
    update_columns = [col for col in display_df.columns if col.endswith("_updated")]
    columns_order = ["city"] + price_columns + update_columns
    columns_order = [col for col in columns_order if col in display_df.columns]
    display_df = display_df[columns_order]

    # Rename columns
    column_mapping = {
        "city": "City",
        "sell_price_min": "Min Sell",
        "sell_price_max": "Max Sell",
        "buy_price_min": "Min Buy",
        "buy_price_max": "Max Buy",
        "sell_price_min_updated": "Min Sell Updated",
        "sell_price_max_updated": "Max Sell Updated",
        "buy_price_min_updated": "Min Buy Updated",
        "buy_price_max_updated": "Max Buy Updated",
    }
    display_df = display_df.rename(columns=column_mapping)

    # Create a styled dataframe
    styled_df = display_df.style.apply(
        lambda x: [
            (
                style_time_cell(val)
                if isinstance(val, str) and ("m ago" in val or "h ago" in val)
                else ""
            )
            for val in x
        ],
        axis=0,
    )

    # Display the styled dataframe
    st.dataframe(
        styled_df,
        use_container_width=True,
        column_config={
            col: st.column_config.NumberColumn(col, format="%d")
            for col in display_df.columns
            if any(
                price_type in col.lower()
                for price_type in ["sell", "buy", "min", "max"]
            )
            and "updated" not in col.lower()
        },
        hide_index=True,
    )


def display_analysis_results(opportunities: List[Dict]):
    if not opportunities:
        st.info("No profitable opportunities found.")
        return

    # Sort opportunities by profit
    sorted_opportunities = sorted(
        opportunities, key=lambda x: x["profit"], reverse=True
    )

    # Display top 11 most profitable opportunities in a 3x4 grid
    st.subheader("🏆 Top 10 Most Profitable Opportunities")

    # Split opportunities into rows of 3
    for i in range(0, min(11, len(sorted_opportunities)), 3):
        cols = st.columns(3)
        row_opportunities = sorted_opportunities[i : min(i + 3, 11)]
        for col, opp in zip(cols, row_opportunities):
            with col:
                display_opportunity_card(opp["item_id"], opp)

    # Display full table of opportunities
    st.subheader("📊 All Market Opportunities")
    df_opportunities = pd.DataFrame(sorted_opportunities)

    # Add last updated columns
    df_opportunities["buy_updated"] = df_opportunities["buy_price_date"].apply(
        lambda x: format_time_ago(get_hours_ago(x)) if x else "N/A"
    )
    df_opportunities["sell_updated"] = df_opportunities["sell_price_date"].apply(
        lambda x: format_time_ago(get_hours_ago(x)) if x else "N/A"
    )

    # Reorder columns for better presentation
    columns = [
        "item_id",
        "profit",
        "buy_city",
        "buy_price",
        "buy_updated",
        "sell_city",
        "sell_price",
        "sell_updated",
    ]
    df_opportunities = df_opportunities[columns]

    # Format numeric columns
    df_opportunities["profit"] = df_opportunities["profit"].map("{:,.0f}".format)
    df_opportunities["buy_price"] = df_opportunities["buy_price"].map("{:,.0f}".format)
    df_opportunities["sell_price"] = df_opportunities["sell_price"].map(
        "{:,.0f}".format
    )

    # Create styled dataframe
    styled_df = df_opportunities.style.apply(
        lambda x: [
            (
                style_time_cell(val)
                if isinstance(val, str) and ("m ago" in val or "h ago" in val)
                else ""
            )
            for val in x
        ],
        axis=0,
    )

    # Display the styled dataframe
    st.dataframe(
        styled_df,
        use_container_width=True,
        column_config={
            "item_id": "Item",
            "profit": "Profit (Silver)",
            "buy_city": "Buy Location",
            "buy_price": "Buy Price",
            "buy_updated": "Buy Updated",
            "sell_city": "Sell Location",
            "sell_price": "Sell Price",
            "sell_updated": "Sell Updated",
        },
        hide_index=True,
    )


def display_opportunity_card(item_id: str, data: Dict):
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image(f"https://render.albiononline.com/v1/item/{item_id}.png", width=60)
    with col2:
        st.markdown(f"**{item_id}**")
        st.markdown(
            f"""
            💰 **Profit:** {data['profit']:,} silver  
            🛒 Buy: {data['buy_city']} at {data['buy_price']:,}  
            💼 Sell: {data['sell_city']} at {data['sell_price']:,}
            """,
            unsafe_allow_html=False,
        )


def display_black_market_results(opportunities: List[Dict]):
    if not opportunities:
        st.info("No profitable Black Market opportunities found.")
        return

    # Sort opportunities by profit
    sorted_opportunities = sorted(
        opportunities, key=lambda x: x["profit"], reverse=True
    )

    # Display top 11 most profitable opportunities in a 3x4 grid
    st.subheader("🏴‍☠️ Top Black Market Flips")

    # Split opportunities into rows of 3
    for i in range(0, min(11, len(sorted_opportunities)), 3):
        cols = st.columns(3)
        row_opportunities = sorted_opportunities[i : min(i + 3, 11)]
        for col, opp in zip(cols, row_opportunities):
            with col:
                display_opportunity_card(opp["item_id"], opp)

    # Display full table of opportunities
    st.subheader("📊 All Black Market Opportunities")
    df_opportunities = pd.DataFrame(sorted_opportunities)

    # Add last updated columns
    if "buy_price_date" in df_opportunities.columns:
        df_opportunities["buy_updated"] = df_opportunities["buy_price_date"].apply(
            lambda x: format_time_ago(get_hours_ago(x)) if x else "N/A"
        )
    if "sell_price_date" in df_opportunities.columns:
        df_opportunities["sell_updated"] = df_opportunities["sell_price_date"].apply(
            lambda x: format_time_ago(get_hours_ago(x)) if x else "N/A"
        )

    # Reorder and rename columns
    columns = [
        "item_id",
        "profit",
        "buy_city",
        "buy_price",
        "buy_updated",
        "sell_city",
        "sell_price",
        "sell_updated",
    ]
    df_opportunities = df_opportunities[columns]

    # Create styled dataframe
    styled_df = df_opportunities.style.apply(
        lambda x: [
            (
                style_time_cell(val)
                if isinstance(val, str) and ("m ago" in val or "h ago" in val)
                else ""
            )
            for val in x
        ],
        axis=0,
    )

    # Display the styled dataframe
    st.dataframe(
        styled_df,
        use_container_width=True,
        column_config={
            "item_id": "Item",
            "profit": st.column_config.NumberColumn("Profit (Silver)", format="%d"),
            "buy_city": "Buy Location",
            "buy_price": st.column_config.NumberColumn("Buy Price", format="%d"),
            "buy_updated": "Buy Updated",
            "sell_city": "Sell Location",
            "sell_price": st.column_config.NumberColumn("Sell Price", format="%d"),
            "sell_updated": "Sell Updated",
        },
        hide_index=True,
    )

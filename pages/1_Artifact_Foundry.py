import streamlit as st
import pandas as pd
import numpy as np
from config.constants import CITIES, BASE_URL, RUNE_ITEMS, SOUL_ITEMS, RELIC_ITEMS, AVALONIAN_ITEMS
from utils.data_fetcher import DataFetcher

st.set_page_config(
    page_title="Artifact Foundry Calculator",
    page_icon="🔨",
    layout="wide"
)

def fetch_prices(item_ids: list, city: str) -> pd.DataFrame:
    """Fetch prices for given item IDs."""
    if city == "Average":
        locations = CITIES
    else:
        locations = [city]
    
    url = f"{BASE_URL}{','.join(item_ids)}.json?locations={','.join(locations)}&qualities=1"
    df = DataFetcher.fetch_artifact_prices(url)
    
    if df.empty:
        return pd.DataFrame()
    
    # If Average is selected, calculate average prices across all cities
    if city == "Average":
        df = df.groupby('item_id').agg({
            'sell_price_min': 'mean',
            'buy_price_max': 'mean'
        }).reset_index()
        df['city'] = 'Average'
    
    return df

def display_price_table(df: pd.DataFrame, title: str, expected_tiers: list, item_ids: list, city: str):
    """Display a price table for the given DataFrame, showing all expected tiers."""
    # Create a DataFrame with all expected tiers
    all_tiers_df = pd.DataFrame({
        'Artifact': expected_tiers,
        'Sell Order (50)': ['No Data'] * len(expected_tiers),
        'Buy Order (50)': ['No Data'] * len(expected_tiers)
    })
    
    if not df.empty:
        # Format the display
        display_df = df.copy()
        display_df = display_df[['item_id', 'sell_price_min', 'buy_price_max']]
        
        # Multiply prices by 50
        display_df['sell_price_min'] = display_df['sell_price_min'] * 50
        display_df['buy_price_max'] = display_df['buy_price_max'] * 50
        
        # Rename columns
        display_df.columns = ['Artifact', 'Sell Order (50)', 'Buy Order (50)']
        
        # Format numeric columns
        for col in ['Sell Order (50)', 'Buy Order (50)']:
            display_df[col] = display_df[col].map("{:,.0f}".format)
        
        # Update all_tiers_df with available data
        for _, row in display_df.iterrows():
            tier = row['Artifact']
            if tier in all_tiers_df['Artifact'].values:
                idx = all_tiers_df[all_tiers_df['Artifact'] == tier].index[0]
                all_tiers_df.at[idx, 'Sell Order (50)'] = row['Sell Order (50)']
                all_tiers_df.at[idx, 'Buy Order (50)'] = row['Buy Order (50)']
    
    # Display the table
    st.subheader(title)
    st.dataframe(
        all_tiers_df,
        use_container_width=True,
        hide_index=True
    )
    
    # Add debug section
    with st.expander("Debug Info"):
        locations = CITIES if city == "Average" else [city]
        url = f"{BASE_URL}{','.join(item_ids)}.json?locations={','.join(locations)}&qualities=1"
        st.code(url, language="text")
        
        st.write("Raw Data Received:")
        if not df.empty:
            st.dataframe(df)
        else:
            st.write("No data received")
        
        st.write("Expected Tiers:")
        st.write(expected_tiers)
        
        st.write("Processed Data:")
        st.dataframe(display_df if not df.empty else pd.DataFrame())

def main():
    st.title("🔨 Artifact Foundry Calculator")
    
    # City selection
    st.write("Select City")
    city = st.selectbox(
        "City",
        ["Average", "Thetford", "Martlock", "Bridgewatch", "Lymhurst", "Fort Sterling", "Caerleon", "Black Market", "Brecilien"],
        key="city"
    )
    
    # Fetch and display prices for each artifact type
    with st.spinner("Fetching artifact prices..."):
        # Runes
        rune_df = fetch_prices(RUNE_ITEMS, city)
        display_price_table(rune_df, "Rune Prices", RUNE_ITEMS, RUNE_ITEMS, city)
        
        # Souls
        soul_df = fetch_prices(SOUL_ITEMS, city)
        display_price_table(soul_df, "Soul Prices", SOUL_ITEMS, SOUL_ITEMS, city)
        
        # Relics
        relic_df = fetch_prices(RELIC_ITEMS, city)
        display_price_table(relic_df, "Relic Prices", RELIC_ITEMS, RELIC_ITEMS, city)
        
        # Avalonian
        avalonian_df = fetch_prices(AVALONIAN_ITEMS, city)
        display_price_table(avalonian_df, "Avalonian Shard Prices", AVALONIAN_ITEMS, AVALONIAN_ITEMS, city)

if __name__ == "__main__":
    main() 
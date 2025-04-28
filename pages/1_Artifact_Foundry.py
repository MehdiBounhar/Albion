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

def fetch_all_cities_data():
    """Fetch and store all artifact data for all cities in session state."""
    all_cities_data = {}
    
    # Fetch data for each city
    for city in CITIES:
        url = f"{BASE_URL}{','.join(RUNE_ITEMS + SOUL_ITEMS + RELIC_ITEMS + AVALONIAN_ITEMS)}.json?locations={city}&qualities=1"
        city_data = DataFetcher.fetch_artifact_prices(url)
        if not city_data.empty:
            all_cities_data[city] = city_data
    
    # Store the data in session state
    st.session_state.all_cities_data = all_cities_data
    
    # Calculate average prices
    if all_cities_data:
        all_data = pd.concat(all_cities_data.values())
        average_data = all_data.groupby('item_id').agg({
            'sell_price_min': 'mean',
            'buy_price_max': 'mean'
        }).reset_index()
        average_data['city'] = 'Average'
        st.session_state.all_cities_data['Average'] = average_data

def get_city_data(city: str) -> dict:
    """Get artifact data for a specific city."""
    if 'all_cities_data' not in st.session_state:
        return {
            'rune_data': pd.DataFrame(),
            'soul_data': pd.DataFrame(),
            'relic_data': pd.DataFrame(),
            'avalonian_data': pd.DataFrame()
        }
    
    city_data = st.session_state.all_cities_data.get(city, pd.DataFrame())
    
    return {
        'rune_data': city_data[city_data['item_id'].isin(RUNE_ITEMS)] if not city_data.empty else pd.DataFrame(),
        'soul_data': city_data[city_data['item_id'].isin(SOUL_ITEMS)] if not city_data.empty else pd.DataFrame(),
        'relic_data': city_data[city_data['item_id'].isin(RELIC_ITEMS)] if not city_data.empty else pd.DataFrame(),
        'avalonian_data': city_data[city_data['item_id'].isin(AVALONIAN_ITEMS)] if not city_data.empty else pd.DataFrame()
    }

def display_price_table(df: pd.DataFrame, title: str, expected_tiers: list):
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
    
    # Initialize session state if not exists
    if 'all_cities_data' not in st.session_state:
        with st.spinner("Fetching prices for all cities..."):
            fetch_all_cities_data()
    
    # City selection
    st.write("Select City")
    city = st.selectbox(
        "City",
        ["Average"] + CITIES,
        key="city"
    )
    
    # Get data for selected city
    city_data = get_city_data(city)
    
    # Display T4 Avalonian Shard price
    t4_shard_data = city_data['avalonian_data'][city_data['avalonian_data']['item_id'] == 'T4_SHARD_AVALONIAN']
    if not t4_shard_data.empty:
        sell_price = t4_shard_data['sell_price_min'].iloc[0] * 50
        buy_price = t4_shard_data['buy_price_max'].iloc[0] * 50
        st.markdown(f"""
        ### T4 Avalonian Shard (50)
        - **Sell Order:** {sell_price:,.0f} silver
        - **Buy Order:** {buy_price:,.0f} silver
        """)
    else:
        st.markdown("""
        ### T4 Avalonian Shard (50)
        - **No data available**
        """)
    
    # Display tables using stored data
    display_price_table(city_data['rune_data'], "Rune Prices", RUNE_ITEMS)
    display_price_table(city_data['soul_data'], "Soul Prices", SOUL_ITEMS)
    display_price_table(city_data['relic_data'], "Relic Prices", RELIC_ITEMS)
    display_price_table(city_data['avalonian_data'], "Avalonian Shard Prices", AVALONIAN_ITEMS)
    
    # Add a button to force refresh data
    if st.button("🔄 Refresh All Data"):
        with st.spinner("Refreshing prices for all cities..."):
            fetch_all_cities_data()
            st.experimental_rerun()

if __name__ == "__main__":
    main()  
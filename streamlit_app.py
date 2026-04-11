import streamlit as st
import pandas as pd

# 1. SETUP
st.set_page_config(page_title="ConfirmAm", page_icon="🛡️")

# YOUR NEW ID
SHEET_ID = "1uQebi8rJgMpIfoXU7JfLcgb8ADa02R3DXoWzoDJC4Qo"
# This URL format is the most stable for mobile apps
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

# 2. DATA LOADING
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = [c.strip().lower() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Waiting for Google Sheet connection... {e}")
        return None

# 3. SIDEBAR
st.sidebar.title("ConfirmAm 🛡️")
st.sidebar.link_button("📦 Track My Order", "https://wa.me/2347046481507", type="primary", use_container_width=True)
menu = st.sidebar.radio("Menu", ["Shopping Mall", "Safety"])

# 4. MAIN SCREEN
if menu == "Shopping Mall":
    st.header("ConfirmAm Mall")
    df = load_data()
    
    if df is not None:
        if df.empty:
            st.warning("No active items found in the sheet.")
        else:
            for i, row in df.iterrows():
                with st.container():
                    st.write(f"### {row.get('name', 'Item')}")
                    st.write(f"**Price:** ₦{row.get('price', 0)}")
                    st.link_button("Buy Now", "https://flutterwave.com/pay/ctppxixgdke7")
                    st.write("---")
    else:
        st.info("Ensure your Google Sheet is set to 'Anyone with the link' and refresh.")

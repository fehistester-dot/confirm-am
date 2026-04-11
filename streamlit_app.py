import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="ConfirmAm Mall", page_icon="🛍️", layout="wide")

# 2. Your Connected Database Link
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Amh_WmVwXCeZhc0h6NesZhBuGZAT0Ch60PuH-BF3xVE/export?format=csv"

def get_mall_data():
    try:
        # Pulling the live data from your Google Sheet
        df = pd.read_csv(SHEET_URL)
        # Standardize the headers (lowercase and no spaces)
        df.columns = df.columns.str.strip().str.lower()
        return df
    except Exception as e:
        # This shows if the sheet is empty or the link isn't shared correctly
        return pd.DataFrame()

# --- THE INTERFACE ---

# Elegant Black and Gold Header
st.markdown("""
    <div style="background-color:#000; color:#d4af37; padding:15px; border-radius:15px; text-align:center; margin-bottom:20px;">
        <h2 style="margin:0;">ConfirmAm Live Mall ✨</h2>
        <p style="margin:0; opacity:0.8; font-size:0.9em;">Secure Escrow Marketplace</p>
    </div>
    """, unsafe_allow_html=True)

data = get_mall_data()

if not data.empty:
    # Creating two columns for a professional mobile shopping experience
    col1, col2 = st.columns(2)
    
    for i, row in data.iterrows():
        # Alternates products between the left and right column
        target_col = col1 if i % 2 == 0 else col2
        
        with target_col:
            # Check for Image URL
            if 'image_url' in row and pd.notnull(row['image_url']):
                st.image(row['image_url'], use_container_width=True)
            else:
                # Placeholder if no image link is provided yet
                st.markdown("""
                    <div style="height:150px; background-color:#f9f9f9; border-radius:15px; display:flex; align-items:center; justify-content:center; border:1px dashed #ccc;">
                        <span style="color:#aaa;">📸 No Photo</span>
                    </div>
                """, unsafe_allow_html=True)
            
            # Verified Badge Logic
            is_verified = str(row.get('verified', '')).strip().upper() == "TRUE"
            badge = "✅" if is_verified else ""
            
            # Product Details Card
            st.markdown(f"""
                <div style="padding:5px 0px 15px 0px;">
                    <p style="font-size:0.75em; color:#666; margin:0;">{row.get('seller', 'Independent Vendor')} {badge}</p>
                    <b style="font-size:1.1em; color:#111;">{row.get('name', 'Fashion Item')}</b>
                    <h3 style="color:#d4af37; margin:0;">₦{row.get('price', 0):,}</h3>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("Buy Now", key=f"buy_{i}"):
                st.toast(f"Starting secure checkout for {row['name']}...")
                st.info("Payment feature connecting soon!")

else:
    # What shows if your Google Sheet is empty or hasn't been filled yet
    st.warning("### 🚧 Showroom Under Construction")
    st.write("We are currently verifying vendors and stocking the mall. Please check back shortly!")
    st.link_button("Add Items to Google Sheet", "https://docs.google.com/spreadsheets/d/1Amh_WmVwXCeZhc0h6NesZhBuGZAT0Ch60PuH-BF3xVE/edit")

# Simple Sidebar
with st.sidebar:
    st.title("ConfirmAm")
    st.write("---")
    st.write("🛡️ **Escrow Protection Active**")
    st.write("Your money is safe until delivery is confirmed.")

import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="ConfirmAm Mall", page_icon="🛍️", layout="wide")

# 2. Connection
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Amh_WmVwXCeZhc0h6NesZhBuGZAT0Ch60PuH-BF3xVE/export?format=csv"

def get_mall_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip().str.lower()
        return df
    except:
        return pd.DataFrame()

# 3. Custom CSS for "The Luxury Look"
st.markdown("""
    <style>
    /* Main background color */
    .stApp { background-color: #fcfcfc; }
    
    /* Product Card Styling */
    .product-card {
        background-color: white;
        padding: 12px;
        border-radius: 15px;
        border: 1px solid #f0f0f0;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.02);
        margin-bottom: 20px;
    }
    
    /* Price Styling */
    .price-text {
        color: #d4af37;
        font-weight: 800;
        font-size: 1.2em;
        margin: 0;
    }

    /* Seller Name & Badge */
    .seller-text {
        color: #888;
        font-size: 0.8em;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div style="background-color:#000; padding:20px; border-radius:15px; text-align:center; margin-bottom:25px;">
        <h2 style="color:#d4af37; margin:0; letter-spacing:1px;">CONFIRMAM MALL</h2>
        <p style="color:white; margin:0; font-size:0.8em; opacity:0.7;">Verified Luxury Marketplace</p>
    </div>
    """, unsafe_allow_html=True)

data = get_mall_data()

if not data.empty:
    # 2-column grid for professional mobile look
    cols = st.columns(2)
    
    for i, row in data.iterrows():
        # Cycle through columns
        with cols[i % 2]:
            # The Card Container
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            
            # 1. Image
            if 'image_url' in row and pd.notnull(row['image_url']):
                st.image(row['image_url'], use_container_width=True)
            else:
                st.markdown('<div style="height:160px; background:#f7f7f7; border-radius:10px; display:flex; align-items:center; justify-content:center; color:#ccc; font-size:0.8em;">📸 No Photo</div>', unsafe_allow_html=True)
            
            # 2. Verified Badge
            is_verified = str(row.get('verified', '')).strip().upper() == "TRUE"
            badge = '<span style="color:#1DA1F2; margin-left:4px;">☑️</span>' if is_verified else ""
            
            # 3. Text Details
            st.markdown(f"""
                <div style="padding-top:10px;">
                    <p class="seller-text">{row.get('seller', 'Vendor')} {badge}</p>
                    <p style="font-weight:600; font-size:1em; margin:0; color:#111; height:40px; overflow:hidden;">{row.get('name', 'Fashion Item')}</p>
                    <p class="price-text">₦{row.get('price', 0):,}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # 4. Action Button
            st.button("Secure Order", key=f"btn_{i}", use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Stocking the showroom... check back in a few minutes!")

# --- FOOTER ---
st.markdown("<p style='text-align:center; color:#aaa; font-size:0.7em; margin-top:50px;'>100% Escrow Protection Active 🛡️</p>", unsafe_allow_html=True)

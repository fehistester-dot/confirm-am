import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="ConfirmAm Marketplace", 
    page_icon="https://i.postimg.cc/mD3WvH5n/Confirm-Am-Logo-Tick.png",
    layout="wide"
)

# 2. ASSETS & DATABASE
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-19BcEQqsLvRKoUX3opcah88GT6veC_8arPqryiJBWs/export?format=csv"
FLUTTERWAVE_LINK = "https://flutterwave.com/pay/ctppxixgdke7"

# ZIMI LINKS
ZIMI_WAVING = "https://i.postimg.cc/9QdS9nRv/Gemini-Generated-Image-5wc5485wc5485wc5-removebg-preview.png"
ZIMI_THINKING = "https://i.postimg.cc/ZKyXbRJ1/Gemini-Generated-Image-5wc5485wc5485wc5-2-removebg-preview.png"
ZIMI_HAPPY = "https://i.postimg.cc/7h5dTP0K/Gemini-Generated-Image-5wc5485wc5485wc5-1-removebg-preview.png"

# 3. Session State
if 'zimi_mood' not in st.session_state:
    st.session_state.zimi_mood = ZIMI_WAVING

# 4. Global Styling
st.markdown(f"""
    <style>
    .stApp {{ background-color: #fcfcfc; }}
    
    /* 5-COLUMN COMPACT PRODUCT CARDS */
    .product-card {{
        background-color: white; 
        padding: 8px; 
        border-radius: 10px;
        border: 1px solid #eee; 
        margin-bottom: 10px; 
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    .price-text {{ color: #1DA1F2; font-weight: 800; font-size: 1.0em; margin: 3px 0; }}
    .hero-box {{ background: #1DA1F2; color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 25px; }}
    .featured-box {{ background: #FFF9E6; border: 2px solid #FFD700; padding: 15px; border-radius: 15px; margin-bottom: 20px; }}
    
    /* THE LARGE SIDE ZIMI (3x size, Side-Anchored) */
    .zimi-float {{
        position: fixed;
        bottom: -20px; 
        right: -50px; 
        z-index: 9999;
        width: 390px;
        filter: drop-shadow(0px 10px 15px rgba(0,0,0,0.2));
        pointer-events: none; /* Allows click-through */
        transition: all 0.5s ease-in-out;
    }}
    </style>
    
    <div class="zimi-float">
        <img src="{st.session_state.zimi_mood}" width="100%">
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.image("https://i.postimg.cc/mD3WvH5n/Confirm-Am-Logo-Tick.png", use_container_width=True)
st.sidebar.markdown("<h2 style='text-align:center;'>ConfirmAm</h2>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.subheader("🌍 International Pricing")
currency = st.sidebar.selectbox("Select Currency", ["NGN (₦)", "USD ($)"])
exchange_rate = 1600 

st.sidebar.markdown("---")
st.sidebar.subheader("📦 Support")
st.sidebar.link_button("Track My Order", "https://wa.me/2347046481507", use_container_width=True)

menu = st.sidebar.radio("Navigation", ["🛍️ Shopping Mall", "🛡️ Safety & Escrow", "📥 Merchant Portal"])

# --- PAGE LOGIC ---

if menu == "🛍️ Shopping Mall":
    st.session_state.zimi_mood = ZIMI_WAVING
    st.markdown('<div class="hero-box"><h1>ConfirmAm Mall</h1><p>Verified Items • Secure Escrow • 10% Protection Fee Included</p></div>', unsafe_allow_html=True)
    
    try:
        data = pd.read_csv(SHEET_URL)
        data.columns = [c.strip().lower() for c in data.columns]

        search_query = st.text_input("🔍 Search products...", "").lower()
        
        if not search_query:
            st.markdown('<div class="featured-box"><b>🌟 Zimi\'s Pick:</b> Highly rated vendor.

import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="ConfirmAm Marketplace", 
    page_icon="🛡️",
    layout="wide"
)

# 2. THE DATABASE LINKS - UPDATED WITH YOUR NEW GID
SHEET_ID = "1VubDpOo8wOWTOeyhgu-9oMlagyTvRZUqDc6wkXIpfTY"

# GID 1271207401 is for your new Form Responses tab
PRODUCTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1271207401"
MERCHANTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1626214553"

FLUTTERWAVE_LINK = "https://flutterwave.com/pay/ctppxixgdke7"

# --- ZIMI IMAGE LINKS ---
ZIMI_SIDEBAR = "https://i.postimg.cc/9QdS9nRv/Gemini-Generated-Image-5wc5485wc5485wc5-removebg-preview.png"
ZIMI_MALL = "https://i.postimg.cc/ZKyXbRJ1/Gemini-Generated-Image-5wc5485wc5485wc5-2-removebg-preview.png"
ZIMI_MERCHANT = "https://i.postimg.cc/7h5dTP0K/Gemini-Generated-Image-5wc5485wc5485wc5-1-removebg-preview.png"

# 3. Enhanced Design & Styling
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    .product-card {
        background-color: white; padding: 12px; border-radius: 15px;
        border: 1px solid #eee; margin-bottom: 20px; text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); transition: 0.3s;
    }
    .product-card:hover { transform: translateY(-5px); box-shadow: 0 8px 15px rgba(0,0,0,0.1); }
    .price-text { color: #1DA1F2; font-weight: 800; font-size: 1.2em; margin: 8px 0; }
    .hero-box { background: linear-gradient(135deg, #1DA1F2 0%, #01579b 100%); color: white; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 25px; }
    .stSidebar [data-testid="stImage"] img { border-radius: 15px; }
    .vendor-tag { background: #e1f5fe; color: #01579b; font-size: 0.7em; padding: 2px 8px; border-radius: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR & GLOBAL SETTINGS ---
st.sidebar.image(ZIMI_SIDEBAR, use_container_width=True)
st.sidebar.markdown("<h2 style='text-align:center;'>ConfirmAm</h2>", unsafe_allow_html=True)

# Currency Toggle
currency = st.sidebar.selectbox("Display Currency", ["🇳🇬 NGN (Naira)", "🇺🇸 USD (Dollar)"])
rate = 1500 # Adjust this manually when the rate changes
symbol = "₦" if "NGN" in currency else "$"

st

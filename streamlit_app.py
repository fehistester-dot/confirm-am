import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. Page Configuration
st.set_page_config(page_title="ConfirmAm Marketplace", page_icon="🛡️", layout="wide")

# 2. THE DATABASE LINKS (Using your specific IDs)
SHEET_ID = "1VubDpOo8wOWTOeyhgu-9oMlagyTvRZUqDc6wkXIpfTY"
PRODUCTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
MERCHANTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1626214553"

# 3. THE MASTER KEY FUNCTION
def get_data(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return pd.read_csv(StringIO(response.text))
    except:
        return pd.DataFrame()

# 4. DESIGN & STYLING (Kept professional and clean)
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    .product-card {
        background-color: white; padding: 15px; border-radius: 15px;
        border: 1px solid #eee; margin-bottom: 20px; text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .price-text { color: #1DA1F2; font-weight: 800; font-size: 1.2em; margin: 8px 0; }
    .hero-box { 
        background: linear-gradient(135deg, #1DA1F2 0%, #01579b 100%); 
        color: white; padding: 40px; border-radius: 15px; text-align: center; margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.title("ConfirmAm 🛡️")
menu = st.sidebar.radio("Navigate", ["🛍️ Shopping Mall", "🏢 Merchant Catalog", "📥 Apply to Sell"])

# --- 1. SHOPPING MALL ---
if menu == "🛍️ Shopping Mall":
    st.markdown('<div class="hero-box"><h1>ConfirmAm Mall</h1><p>Premium Selections • Verified Vendors • Secure Payments</p></div>', unsafe_allow_html=True)
    
    try:
        data = get_data(PRODUCTS_URL)
        if not data.empty:
            data.columns = [c.strip().lower() for c in data.columns]
            cols = st.columns(2) 
            for i, row in data.iterrows():
                with cols[i % 2]:
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    st.image(row.get('image_url', ''), use_container_width=True)
                    st.write(f"**{row.get('name', 'Product')}**")
                    st.markdown(f'<p class="price-text">₦{row.get("price", 0):,}</p>', unsafe_allow_html=True)
                    st.link_button("Buy Now", "https://flutterwave.com/pay/ctppxixgdke7", use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("The Mall is currently being updated. Please refresh in a moment!")
    except:
        st.error("Database Connection Busy. Please Refresh.")

# --- 2. MERCHANT CATALOG ---
elif menu == "🏢 Merchant Catalog":
    st.header("Verified Partners")
    try:
        m_data = get_data(MERCHANTS_URL)
        if not m_data.empty:
            m_data.columns = [c.strip().lower() for c in m_data.columns]
            for _, row in m_data.iterrows():
                with st.expander(f"✅ {row.iloc[0]}"):
                    st.write(f"**Niche:** {row.get('category', row.get('niche', 'General'))}")
                    st.write(f"**Socials:** {row.get('socials', row.get('instagram/tiktok handle', 'Contact Admin'))}")
        else:
            st.info("Zimi is currently vetting new merchants. Check back soon!")
    except:
        st.error("Could not load merchants.")

# --- 3. APPLY TO SELL ---
elif menu == "📥 Apply to Sell":
    st.title("Partner with ConfirmAm")
    with st.form("Merchant Application"):
        b_name = st.text_input("Business Name")
        b_cat = st.selectbox("Niche", ["Fashion", "Electronics", "Beauty", "Services", "Other"])
        b_social = st.text_input("Instagram/TikTok Handle")
        
        if st.form_submit_button("Submit Application"):
            st.success("Application received!")
            st.link_button("Finalize on WhatsApp", f"https://wa.me/2347046481507?text=Application:%20{b_name}")

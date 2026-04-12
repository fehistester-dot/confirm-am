import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. Page Configuration
st.set_page_config(page_title="ConfirmAm Marketplace", page_icon="🛡️", layout="wide")

# 2. THE DATABASE LINKS
SHEET_ID = "1VubDpOo8wOWTOeyhgu-9oMlagyTvRZUqDc6wkXIpfTY"
# gid=0 is usually Products. REPLACE 1626214553 WITH YOUR ACTUAL MERCHANT GID
PRODUCTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
MERCHANTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1626214553"

# --- MASTER KEY CONNECTION ---
def load_sheet_data(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            df = pd.read_csv(StringIO(response.text), on_bad_lines='skip')
            return df.dropna(how='all')
        return pd.DataFrame()
    except:
        return pd.DataFrame()

# 3. Styling
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    .product-card {
        background-color: white; padding: 15px; border-radius: 15px;
        border: 1px solid #eee; margin-bottom: 20px; text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .price-text { color: #1DA1F2; font-weight: 800; font-size: 1.2em; }
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
    st.markdown('<div class="hero-box"><h1>ConfirmAm Mall</h1><p>Verified Vendors • Secure Payments</p></div>', unsafe_allow_html=True)
    data = load_sheet_data(PRODUCTS_URL)
    
    if not data.empty:
        data.columns = [c.strip().lower() for c in data.columns]
        cols = st.columns(2) 
        for i, row in data.iterrows():
            with cols[i % 2]:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                img_url = row.get('image_url', row.get('image', ''))
                if pd.notna(img_url) and str(img_url).strip() != "":
                    try: st.image(str(img_url), use_container_width=True)
                    except: st.warning("Image link error")
                
                st.write(f"**{row.get('name', 'Product')}**")
                try:
                    price = float(row.get('price', 0)) * 1.05
                    st.markdown(f'<p class="price-text">₦{price:,.0f}</p>', unsafe_allow_html=True)
                except: st.write("Price: TBD")
                
                st.link_button("Buy Now", "https://flutterwave.com/pay/ctppxixgdke7", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("The Mall is being updated...")

# --- 2. MERCHANT CATALOG (THE FIXED PART) ---
elif menu == "🏢 Merchant Catalog":
    st.header("Verified Partners")
    m_data = load_sheet_data(MERCHANTS_URL)
    
    if not m_data.empty:
        # Instead of looking for names, we take the columns by position
        # Column 0 = Name, Column 1 = Category, Column 2 = Socials
        for _, row in m_data.iterrows():
            biz_name = row.iloc[0] # Grab first column
            if pd.notna(biz_name) and str(biz_name).strip() != "":
                with st.expander(f"✅ {biz_name}"):
                    # Try to show secondary info if it exists
                    if len(row) > 1: st.write(f"**Niche:** {row.iloc[1]}")
                    if len(row) > 2: st.write(f"**Socials:** {row.iloc[2]}")
    else:
        # This message shows if the URL is wrong or the sheet is empty
        st.error("No merchants found. Please verify the 'GID' number in the code.")

# --- 3. APPLY TO SELL ---
elif menu == "📥 Apply to Sell":
    st.title("Partner with ConfirmAm")
    with st.form("Apply"):
        name = st.text_input("Business Name")
        if st.form_submit_button("Submit"):
            st.link_button("Finalize on WhatsApp", f"https://wa.me/2347046481507?text=Apply:{name}")

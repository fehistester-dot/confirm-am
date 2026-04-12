import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. Page Configuration
st.set_page_config(
    page_title="ConfirmAm Marketplace", 
    page_icon="🛡️",
    layout="wide"
)

# 2. THE DATABASE LINKS (Using the more stable /export method)
SHEET_ID = "1-19BcEQqsLvRKoUX3opcah88GT6veC_8arPqryiJBWs"
PRODUCTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
MERCHANTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1626214553"
FLUTTERWAVE_LINK = "https://flutterwave.com/pay/ctppxixgdke7"

# --- ZIMI IMAGE LINKS ---
ZIMI_SIDEBAR = "https://i.postimg.cc/9QdS9nRv/Gemini-Generated-Image-5wc5485wc5485wc5-removebg-preview.png"
ZIMI_MALL = "https://i.postimg.cc/ZKyXbRJ1/Gemini-Generated-Image-5wc5485wc5485wc5-2-removebg-preview.png"

# --- THE MASTER KEY CONNECTION ---
def load_sheet_data(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        df = pd.read_csv(StringIO(response.text), on_bad_lines='skip')
        df.columns = [c.strip().lower() for c in df.columns]
        return df.dropna(how='all')
    except:
        return pd.DataFrame()

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
    .vendor-tag { background: #e1f5fe; color: #01579b; font-size: 0.7em; padding: 2px 8px; border-radius: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR & GLOBAL SETTINGS ---
st.sidebar.image(ZIMI_SIDEBAR, use_container_width=True)
st.sidebar.markdown("<h2 style='text-align:center;'>ConfirmAm</h2>", unsafe_allow_html=True)

# INTERNATIONAL CURRENCY TOGGLE
currency = st.sidebar.selectbox("Display Currency", ["🇳🇬 NGN (Naira)", "🇺🇸 USD (Dollar)"])
rate = 1500 
symbol = "₦" if "NGN" in currency else "$"

st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigate", ["🛍️ Shopping Mall", "🏢 Merchant Catalog", "🛡️ How Escrow Works", "📥 Apply to Sell"])

# --- 1. SHOPPING MALL ---
if menu == "🛍️ Shopping Mall":
    st.markdown('<div class="hero-box"><h1>ConfirmAm Mall</h1><p>Verified Vendors • Escrow Protected • Global Shipping</p></div>', unsafe_allow_html=True)
    
    # SEARCH BAR
    search_query = st.text_input("🔍 Search for products, brands, or categories...", "").lower()

    data = load_sheet_data(PRODUCTS_URL)
    
    if not data.empty:
        # Filter Logic
        if search_query:
            data = data[data['name'].str.lower().str.contains(search_query, na=False) | 
                        data['seller'].str.lower().str.contains(search_query, na=False)]

        # 5 COLUMN GRID
        cols = st.columns(5)
        for i, (idx, row) in enumerate(data.iterrows()):
            with cols[i % 5]:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                
                # Image with Crash Protection
                img = row.get('image_url', '')
                try: st.image(img, use_container_width=True)
                except: st.warning("Image Loading...")
                
                # HIDDEN 5% COMMISSION LOGIC (Applied silently)
                # This ensures you get your 5% while the customer just sees one price
                try:
                    base_price = float(row.get('price', 0))
                    final_amt = base_price * 1.05 # Adding 5% commission
                except:
                    final_amt = 0
                
                display_price = final_amt if symbol == "₦" else (final_amt / rate)
                
                st.markdown(f"""
                    <span class="vendor-tag">👤 {row.get('seller', 'Verified')}</span>
                    <b style="font-size:0.9em; display:block; margin-top:10px; height:40px; overflow:hidden;">{row.get('name', 'Product')}</b>
                    <p class="price-text">{symbol}{display_price:,.0f}</p>
                """, unsafe_allow_html=True)
                
                st.link_button("Instant Buy", FLUTTERWAVE_LINK, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Zimi is refreshing the stock... please refresh in a moment.")

# --- 2. MERCHANT CATALOG ---
elif menu == "🏢 Merchant Catalog":
    st.title("Verified Partners")
    m_data = load_sheet_data(MERCHANTS_URL)
    
    if not m_data.empty:
        for _, row in m_data.iterrows():
            biz_name = row.iloc[0]
            if pd.notna(biz_name):
                with st.expander(f"✅ {biz_name}"):
                    st.write(f"**Niche:** {row.get('category', row.get('niche', 'General'))}")
                    st.write(f"**Handle:** {row.get('socials', 'Contact Support')}")
                    st.caption("Status: Active Verified Merchant")
    else:
        st.warning("Merchant directory is updating...")

# --- 3. SAFETY & ESCROW ---
elif menu == "🛡️ How Escrow Works":
    st.header("The Zimi Guarantee")
    st.markdown("""
    ### Our 5% Secure System
    * **For Buyers:** Your money is held safely until you confirm delivery.
    * **For Sellers:** You are guaranteed payment once the job is done.
    * **The Fee:** A small 5% service fee is included in every transaction to cover our legal protection and 24/7 support.
    """)
    st.link_button("Speak to an Agent", "https://wa.me/2347046481507")

# --- 4. MERCHANT FORM (APPLY TO SELL) ---
elif menu == "📥 Apply to Sell":
    st.title("Partner with ConfirmAm")
    with st.form("Merchant Application"):
        st.write("Submit your details to start selling under our protection.")
        b_name = st.text_input("Business Name")
        b_cat = st.selectbox("Category", ["Fashion", "Electronics", "Beauty", "Home", "Other"])
        b_social = st.text_input("Instagram/TikTok Handle")
        
        if st.form_submit_button("Submit Application"):
            st.success("Application started!")
            msg = f"Hello Zimi, I want to apply as a merchant. Business: {b_name}, Category: {b_cat}"
            st.link_button("Verify on WhatsApp", f"https://wa.me/2347046481507?text={msg}")

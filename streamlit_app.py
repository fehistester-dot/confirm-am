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

# 2. THE DATABASE LINKS
SHEET_ID = "1-19BcEQqsLvRKoUX3opcah88GT6veC_8arPqryiJBWs"
PRODUCTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
MERCHANTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1626214553"
FLUTTERWAVE_LINK = "https://flutterwave.com/pay/ctppxixgdke7"

# --- ZIMI IMAGE LINKS ---
ZIMI_SIDEBAR = "https://i.postimg.cc/9QdS9nRv/Gemini-Generated-Image-5wc5485wc5485wc5-removebg-preview.png"

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

# 3. Styling
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    .product-card {
        background-color: white; padding: 12px; border-radius: 15px;
        border: 1px solid #eee; margin-bottom: 20px; text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); transition: 0.3s;
    }
    .price-text { color: #1DA1F2; font-weight: 800; font-size: 1.2em; margin: 8px 0; }
    .hero-box { background: linear-gradient(135deg, #1DA1F2 0%, #01579b 100%); color: white; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 25px; }
    .vendor-tag { background: #e1f5fe; color: #01579b; font-size: 0.7em; padding: 2px 8px; border-radius: 20px; font-weight: bold; }
    
    /* Photo-Match Form Styling */
    div[data-testid="stForm"] {
        border: 1px solid #eee;
        padding: 20px;
        border-radius: 15px;
        background-color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR & GLOBAL SETTINGS ---
st.sidebar.image(ZIMI_SIDEBAR, use_container_width=True)
currency = st.sidebar.selectbox("Display Currency", ["🇳🇬 NGN (Naira)", "🇺🇸 USD (Dollar)"])
rate = 1500 
symbol = "₦" if "NGN" in currency else "$"

st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigate", ["🛍️ Shopping Mall", "🏢 Merchant Catalog", "🛡️ How Escrow Works", "📥 Apply to Sell"])

# --- 1. SHOPPING MALL ---
if menu == "🛍️ Shopping Mall":
    st.markdown('<div class="hero-box"><h1>ConfirmAm Mall</h1><p>Verified Vendors • Escrow Protected</p></div>', unsafe_allow_html=True)
    search_query = st.text_input("🔍 Search for products, brands, or categories...", "").lower()

    data = load_sheet_data(PRODUCTS_URL)
    if not data.empty:
        if search_query:
            data = data[data['name'].str.lower().str.contains(search_query, na=False)]

        cols = st.columns(5) # 5 COLUMN GRID
        for i, (idx, row) in enumerate(data.iterrows()):
            with cols[i % 5]:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                try: st.image(row.get('image_url', ''), use_container_width=True)
                except: st.warning("Image Loading...")
                
                # Hidden Admin Commission (5%)
                try:
                    price = float(row.get('price', 0)) * 1.05
                except:
                    price = 0
                
                display_price = price if symbol == "₦" else (price / rate)
                st.markdown(f"""
                    <span class="vendor-tag">👤 {row.get('seller', 'Verified')}</span>
                    <b style="font-size:0.9em; display:block; margin-top:10px;">{row.get('name', 'Product')}</b>
                    <p class="price-text">{symbol}{display_price:,.0f}</p>
                """, unsafe_allow_html=True)
                st.link_button("Instant Buy", FLUTTERWAVE_LINK, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

# --- 2. MERCHANT CATALOG ---
elif menu == "🏢 Merchant Catalog":
    st.title("Verified Partners")
    m_data = load_sheet_data(MERCHANTS_URL)
    if not m_data.empty:
        for _, row in m_data.iterrows():
            with st.expander(f"✅ {row.iloc[0]}"):
                st.write(f"**Niche:** {row.get('category', 'General')}")
                st.write(f"**Handle:** {row.get('socials', 'Contact Support')}")

# --- 3. SAFETY ---
elif menu == "🛡️ How Escrow Works":
    st.header("The Zimi Guarantee")
    st.write("We protect both parties with a secure 5% escrow service.")

# --- 4. APPLY TO SELL (MATCHED TO PHOTO) ---
elif menu == "📥 Apply to Sell":
    st.markdown("### Join Nigeria's most trusted escrow marketplace.")
    
    with st.form("Merchant Application"):
        b_name = st.text_input("Business Name")
        b_niche = st.selectbox("Niche", ["Fashion", "Electronics", "Beauty", "Home", "Other"])
        b_email = st.text_input("Email Address")
        b_social = st.text_input("Instagram/TikTok Handle")
        b_phone = st.text_input("WhatsApp Number")
        
        # Centered Submit Button
        submitted = st.form_submit_button("Submit Application")
        
        if submitted:
            if b_name and b_phone:
                st.success("Application received! Click below to finalize.")
                whatsapp_msg = f"Business: {b_name}%0ANiche: {b_niche}%0ASocial: {b_social}"
                st.link_button("Finalize on WhatsApp", f"https://wa.me/2347046481507?text={whatsapp_msg}")
            else:
                st.error("Please fill in Business Name and WhatsApp Number.")

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
SHEET_ID_PRODUCTS = "1VubDpOo8wOWTOeyhgu-9oMlagyTvRZUqDc6wkXIpfTY"
SHEET_ID_MERCHANTS = "1-19BcEQqsLvRKoUX3opcah88GT6veC_8arPqryiJBWs"

PRODUCTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_PRODUCTS}/export?format=csv&gid=0"
MERCHANTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_MERCHANTS}/export?format=csv&gid=0"

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
    .vendor-tag { background: #e1f5fe; color: #01579b; font-size: 0.7em; padding: 2px 8px; border-radius: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Helper function to bypass Google's "Stranger" block
def load_data(url):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    return pd.read_csv(StringIO(response.text))

# --- SIDEBAR ---
st.sidebar.image(ZIMI_SIDEBAR, use_container_width=True)
st.sidebar.markdown("<h2 style='text-align:center;'>ConfirmAm</h2>", unsafe_allow_html=True)

currency = st.sidebar.selectbox("Display Currency", ["🇳🇬 NGN (Naira)", "🇺🇸 USD (Dollar)"])
rate = 1500 
symbol = "₦" if "NGN" in currency else "$"

st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigate", ["🛍️ Shopping Mall", "🏢 Merchant Catalog", "🛡️ How Escrow Works", "📥 Apply to Sell"])

# --- 1. SHOPPING MALL ---
if menu == "🛍️ Shopping Mall":
    st.markdown('<div class="hero-box"><h1>ConfirmAm Mall</h1><p>Premium Selections • Verified Vendors • Secure Payments</p></div>', unsafe_allow_html=True)
    
    try:
        data = load_data(PRODUCTS_URL)
        data.columns = [c.strip().lower() for c in data.columns]
        
        if data.empty:
            st.info("The Mall is currently being stocked. Check back soon!")
        else:
            cols = st.columns(5)
            for i, row in data.iterrows():
                with cols[i % 5]:
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    st.image(row.get('image_url', ''), use_container_width=True)
                    
                    price = float(row.get('price', 0)) * 1.05 
                    display_price = price if symbol == "₦" else (price / rate)
                    
                    st.markdown(f"""
                        <span class="vendor-tag">👤 {row.get('seller', 'Verified Seller')}</span>
                        <b style="font-size:0.9em; display:block; margin-top:10px; height:40px; overflow:hidden;">{row.get('name', 'Product')}</b>
                        <p class="price-text">{symbol}{display_price:,.0f}</p>
                    """, unsafe_allow_html=True)
                    st.link_button("Instant Buy", FLUTTERWAVE_LINK, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error("Connecting to Zimi Database... please refresh.")

# --- 2. MERCHANT CATALOG ---
elif menu == "🏢 Merchant Catalog":
    col_m1, col_m2 = st.columns([1, 4])
    with col_m1: st.image(ZIMI_MERCHANT, width=120)
    with col_m2: st.title("Verified Partners")

    try:
        m_data = load_data(MERCHANTS_URL)
        m_data.columns = m_data.columns.str.strip().str.lower()
        
        cat_col = 'category' if 'category' in m_data.columns else 'niche'
        
        if cat_col in m_data.columns:
            for cat in m_data[cat_col].unique():
                if pd.isna(cat): continue
                with st.expander(f"📁 {str(cat).upper()} VENDORS", expanded=True):
                    cat_vendors = m_data[m_data[cat_col] == cat]
                    for _, m in cat_vendors.iterrows():
                        v_name = m.iloc[0]
                        v_social = m.get('socials', m.get('instagram/tiktok handle', 'No link'))
                        st.markdown(f"✅ **{v_name}** | `{v_social}`")
    except:
        st.warning("Merchant directory is updating...")

# --- 3. SAFETY ---
elif menu == "🛡️ How Escrow Works":
    st.image(ZIMI_SIDEBAR, width=150)
    st.header("The Zimi Guarantee")
    st.write("We hold the funds. You get the goods. Only then do we pay the vendor.")

# --- 4. APPLY TO SELL ---
elif menu == "📥 Apply to Sell":
    st.title("Partner with ConfirmAm")
    with st.form("Merchant Form"):
        b_name = st.text_input("Business Name")
        b_cat = st.selectbox("Niche", ["Fashion", "Electronics", "Beauty", "Services", "Other"])
        b_email = st.text_input("Email Address")
        b_social = st.text_input("Instagram/TikTok Handle")
        b_phone = st.text_input("WhatsApp Number")
        
        if st.form_submit_button("Submit Application"):
            msg = f"App:%20{b_name}%0ACat:%20{b_cat}%0AEmail:%20{b_email}"
            st.success("Application received!")
            st.link_button("Finalize on WhatsApp", f"https://wa.me/2347046481507?text={msg}")

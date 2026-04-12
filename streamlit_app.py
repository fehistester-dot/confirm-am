import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. Page Configuration
st.set_page_config(page_title="ConfirmAm Marketplace", page_icon="🛡️", layout="wide")

# 2. THE DATABASE LINKS
SHEET_ID = "1VubDpOo8wOWTOeyhgu-9oMlagyTvRZUqDc6wkXIpfTY"
# Fixed: Standardized the Export URLs
PRODUCTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
MERCHANTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1626214553"

FLUTTERWAVE_LINK = "https://flutterwave.com/pay/ctppxixgdke7"
ZIMI_SIDEBAR = "https://i.postimg.cc/9QdS9nRv/Gemini-Generated-Image-5wc5485wc5485wc5-removebg-preview.png"

# --- FIX: THE MASTER KEY CONNECTION ---
def load_sheet_data(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        df = pd.read_csv(StringIO(response.text), on_bad_lines='skip')
        df.columns = [c.strip().lower() for c in df.columns]
        return df.dropna(how='all') # Removes empty rows
    except:
        return pd.DataFrame()

# 3. Styling (Your original styles preserved)
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
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.image(ZIMI_SIDEBAR, use_container_width=True)
menu = st.sidebar.radio("Navigate", ["🛍️ Shopping Mall", "🏢 Merchant Catalog", "🛡️ How Escrow Works", "📥 Apply to Sell"])

# --- 1. SHOPPING MALL ---
if menu == "🛍️ Shopping Mall":
    st.markdown('<div class="hero-box"><h1>ConfirmAm Mall</h1><p>Verified Vendors • Secure Payments</p></div>', unsafe_allow_html=True)
    search_query = st.text_input("🔍 Search products...", "").lower()

    data = load_sheet_data(PRODUCTS_URL)
    
    if not data.empty:
        if search_query:
            data = data[data['name'].str.lower().str.contains(search_query, na=False)]

        cols = st.columns(2 if st.sidebar.checkbox("Mobile View", True) else 5)
        for i, (idx, row) in enumerate(data.iterrows()):
            with cols[i % len(cols)]:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                # Fixed: Safer image fetching
                img = row.get('image_url', row.get('image', ''))
                st.image(img if pd.notna(img) else '', use_container_width=True)
                
                try:
                    price = float(row.get('price', 0)) * 1.05
                except:
                    price = 0
                
                st.markdown(f"""
                    <b style="font-size:0.9em; display:block; margin-top:10px;">{row.get('name', 'Product')}</b>
                    <p class="price-text">₦{price:,.0f}</p>
                """, unsafe_allow_html=True)
                st.link_button("Instant Buy", FLUTTERWAVE_LINK, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("Could not connect to database. Check Sheet sharing settings.")

# --- 2. MERCHANT CATALOG ---
elif menu == "🏢 Merchant Catalog":
    st.title("Verified Partners")
    m_data = load_sheet_data(MERCHANTS_URL)
    
    if not m_data.empty:
        for _, m in m_data.iterrows():
            # Fixed: More robust name detection
            biz_name = m.iloc[0] 
            if pd.notna(biz_name):
                with st.container():
                    st.markdown(f"✅ **{biz_name}**")
                    handle = m.get('socials', m.get('instagram/tiktok handle', 'Contact Admin'))
                    st.caption(f"Handle: {handle}")
                    st.markdown("---")
    else:
        st.warning("Merchant directory is updating...")

# --- 3. SAFETY & 4. APPLY (Kept your logic) ---
elif menu == "🛡️ How Escrow Works":
    st.header("The Zimi Guarantee")
    st.write("1. We hold the money. 2. You get the goods. 3. Vendor gets paid.")

elif menu == "📥 Apply to Sell":
    st.title("Partner with ConfirmAm")
    with st.form("Apply"):
        name = st.text_input("Business Name")
        if st.form_submit_button("Submit"):
            st.success("Redirecting...")
            st.link_button("Finish on WhatsApp", f"https://wa.me/2347046481507?text=Apply:{name}")

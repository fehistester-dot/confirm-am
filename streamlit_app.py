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
# We pull by sheet name now to ensure the Merchant info loads correctly
PRODUCTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&sheet=Sheet1"
MERCHANTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&sheet=merchants"
FLUTTERWAVE_LINK = "https://flutterwave.com/pay/ctppxixgdke7"

# --- ZIMI IMAGE LINKS ---
ZIMI_SIDEBAR = "https://i.postimg.cc/9QdS9nRv/Gemini-Generated-Image-5wc5485wc5485wc5-removebg-preview.png"

# --- THE MASTER KEY CONNECTION ---
def load_sheet_data(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        df = pd.read_csv(StringIO(response.text), on_bad_lines='skip')
        # Clean column names
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df.dropna(how='all')
    except Exception as e:
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
    .product-card:hover { transform: translateY(-5px); box-shadow: 0 8px 15px rgba(0,0,0,0.1); }
    .price-text { color: #1DA1F2; font-weight: 800; font-size: 1.2em; margin: 8px 0; }
    .hero-box { background: linear-gradient(135deg, #1DA1F2 0%, #01579b 100%); color: white; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 25px; }
    .vendor-tag { background: #e1f5fe; color: #01579b; font-size: 0.7em; padding: 2px 8px; border-radius: 20px; font-weight: bold; }
    
    div[data-testid="stForm"] {
        border: 1px solid #eee; padding: 20px; border-radius: 15px; background-color: white;
    }
    .safety-card {
        background-color: #f0f9ff; padding: 20px; border-left: 5px solid #1DA1F2; border-radius: 10px; margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR & GLOBAL SETTINGS ---
st.sidebar.image(ZIMI_SIDEBAR, use_container_width=True)
currency = st.sidebar.selectbox("Display Currency", ["🇳🇬 NGN (Naira)", "🇺🇸 USD (Dollar)"])
rate = 1500 
symbol = "₦" if "NGN" in currency else "$"

st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigate", ["🛍️ Shopping Mall", "🏢 Merchant Catalog", "🛡️ How Escrow Works", "📥 Apply to Sell", "📞 Contact Support"])

# --- 1. SHOPPING MALL ---
if menu == "🛍️ Shopping Mall":
    st.markdown('<div class="hero-box"><h1>ConfirmAm Mall</h1><p>Verified Vendors • Escrow Protected</p></div>', unsafe_allow_html=True)
    search_query = st.text_input("🔍 Search for products, brands, or categories...", "").lower()

    data = load_sheet_data(PRODUCTS_URL)
    if not data.empty:
        if search_query:
            # Check for name or seller column safely
            data = data[data.apply(lambda row: search_query in str(row.values).lower(), axis=1)]

        cols = st.columns(5)
        for i, (idx, row) in enumerate(data.iterrows()):
            with cols[i % 5]:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                img_url = row.get('image_url', row.get('image', ''))
                try: st.image(img_url, use_container_width=True)
                except: st.warning("Image Loading...")
                
                # INVISIBLE ADMIN COMMISSION (5%)
                try:
                    raw_p = str(row.get('price', 0)).replace(',', '')
                    price = float(raw_p) * 1.05
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
    else:
        st.info("Zimi is stocking the shelves... Please refresh.")

# --- 2. MERCHANT CATALOG (ENHANCED LOADING) ---
elif menu == "🏢 Merchant Catalog":
    st.title("Verified Partners")
    st.write("Vetted merchants active on ConfirmAm.")
    m_data = load_sheet_data(MERCHANTS_URL)
    
    if not m_data.empty:
        for _, row in m_data.iterrows():
            # Brute force: get first non-empty value as name
            vals = [v for v in row.values if pd.notna(v) and str(v).strip() != ""]
            if vals:
                name = str(vals[0]).upper()
                with st.expander(f"✅ {name}"):
                    st.write(f"**Niche:** {row.get('niche', row.get('category', 'General Vendor'))}")
                    st.write(f"**Status:** Verified Active Merchant")
                    st.markdown("*Escrow Protection: Enabled*")
    else:
        st.warning("Ensure your Google Sheet tab is named 'merchants' exactly.")

# --- 3. SAFETY (COMMISSION HIDDEN FROM BUYERS) ---
elif menu == "🛡️ How Escrow Works":
    st.header("The Zimi Guarantee")
    st.write("ConfirmAm uses a secure Escrow system to make sure your shopping is 100% safe.")
    
    st.markdown("""
    <div class="safety-card">
    <h4>1. Secure Payment</h4>
    <p>We hold your payment in a neutral vault. Your money never goes directly to the seller until you are happy.</p>
    </div>
    <div class="safety-card">
    <h4>2. Delivery Verification</h4>
    <p>The merchant ships your product. You have time to inspect it upon arrival.</p>
    </div>
    <div class="safety-card">
    <h4>3. Happy Ending</h4>
    <p>Once you confirm the order is perfect, we pay the merchant. If not, we refund you.</p>
    </div>
    """, unsafe_allow_html=True)

# --- 4. APPLY TO SELL (COMMISSION VISIBLE TO SELLERS) ---
elif menu == "📥 Apply to Sell":
    st.markdown("### Become a Verified Merchant")
    # Admin Note: Keeping the fee visible only for those wanting to sell
    st.warning("Merchant Policy: A 5% escrow commission is deducted from successful sales to cover legal protection and payment processing.")
    
    with st.form("Merchant Application"):
        b_name = st.text_input("Business Name")
        b_niche = st.selectbox("Niche", ["Fashion", "Electronics", "Beauty", "Home", "Other"])
        b_email = st.text_input("Email Address")
        b_phone = st.text_input("WhatsApp Number")
        
        submitted = st.form_submit_button("Submit Application")
        if submitted:
            if b_name and b_phone:
                st.success("Application started!")
                msg = f"New%20Merchant%20App:%20{b_name}%0ANiche:%20{b_niche}"
                st.link_button("Send Documents via WhatsApp", f"https://wa.me/2347046481507?text={msg}")

# --- 5. CONTACT SUPPORT ---
elif menu == "📞 Contact Support":
    st.header("Dispute Resolution")
    st.link_button("Chat with Admin", "https://wa.me/2347046481507")

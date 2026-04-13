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

# 2. THE DATABASE LINKS & CONFIG
PRODUCT_SHEET_ID = "1-19BcEQqsLvRKoUX3opcah88GT6veC_8arPqryiJBWs"
MERCHANT_SHEET_ID = "1WniAk7CLPVev8qGGwFlah6SwnTeDUT1qJhHM3XslSXU"
WHATSAPP_NUMBER = "2349136533490"  # Updated Number

PRODUCTS_URL = f"https://docs.google.com/spreadsheets/d/{PRODUCT_SHEET_ID}/export?format=csv&gid=0"
MERCHANTS_URL = f"https://docs.google.com/spreadsheets/d/{MERCHANT_SHEET_ID}/export?format=csv&gid=0"
FLUTTERWAVE_LINK = "https://flutterwave.com/pay/ctppxixgdke7"

# --- ZIMI & CREW IMAGE LINKS ---
ZIMI_SIDEBAR = "https://i.postimg.cc/9QdS9nRv/Gemini-Generated-Image-5wc5485wc5485wc5-removebg-preview.png"
# Assigning different characters to sections
CAPTAIN_ZIMI = ZIMI_SIDEBAR
AUDITOR_LEXI = "https://i.postimg.cc/9QdS9nRv/Gemini-Generated-Image-5wc5485wc5485wc5-removebg-preview.png" # Using same for now, replace with actual links if you have them!
SUPPORT_MAX = "https://i.postimg.cc/9QdS9nRv/Gemini-Generated-Image-5wc5485wc5485wc5-removebg-preview.png"

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
    .character-header {
        display: flex; align-items: center; gap: 20px; background: white; padding: 15px; border-radius: 15px; border: 1px solid #eee; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR & GLOBAL SETTINGS ---
st.sidebar.image(ZIMI_SIDEBAR, use_container_width=True)
st.sidebar.markdown(f"**Chat with Zimi:** [Click Here](https://wa.me/{WHATSAPP_NUMBER})")
currency = st.sidebar.selectbox("Display Currency", ["🇳🇬 NGN (Naira)", "🇺🇸 USD (Dollar)"])
rate = 1500 
symbol = "₦" if "NGN" in currency else "$"

st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigate", ["🛍️ Shopping Mall", "🏢 Merchant Catalog", "🛡️ How Escrow Works", "📥 Apply to Sell", "📢 Advertise Product", "📞 Contact Support"])

# --- 1. SHOPPING MALL ---
if menu == "🛍️ Shopping Mall":
    st.markdown(f"""
        <div class="character-header">
            <img src="{CAPTAIN_ZIMI}" width="100">
            <div>
                <h1 style="margin:0; color:#1DA1F2;">ConfirmAm Mall</h1>
                <p style="margin:0; color:#666;"><b>Captain Zimi:</b> "I've personally vetted these deals for you!"</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    search_query = st.text_input("🔍 Search for products, brands, or categories...", "").lower()

    data = load_sheet_data(PRODUCTS_URL)
    if not data.empty:
        if search_query:
            data = data[data['name'].str.lower().str.contains(search_query, na=False)]

        cols = st.columns(5)
        for i, (idx, row) in enumerate(data.iterrows()):
            with cols[i % 5]:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                img_url = row.get('image_url', row.get('image', ''))
                try: st.image(img_url, use_container_width=True)
                except: st.warning("Image Loading...")
                
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
    else:
        st.info("Zimi is stocking the shelves... Please refresh.")

# --- 2. MERCHANT CATALOG ---
elif menu == "🏢 Merchant Catalog":
    st.markdown(f"""
        <div class="character-header">
            <img src="{AUDITOR_LEXI}" width="90">
            <div>
                <h2 style="margin:0;">Verified Partners</h2>
                <p style="margin:0; color:#666;"><b>Lexi the Auditor:</b> "Every merchant here has passed our 10-point safety check."</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    m_data = load_sheet_data(MERCHANTS_URL)
    if not m_data.empty:
        for _, row in m_data.iterrows():
            name_val = row.iloc[0] if pd.notna(row.iloc[0]) else "Verified Business"
            with st.expander(f"✅ {str(name_val).upper()}"):
                niche = row.get('niche', row.get('category', 'General Vendor'))
                social = row.get('socials', row.get('instagram', 'Verified'))
                st.write(f"**Niche:** {niche}")
                st.write(f"**Social:** `{social}`")
                st.markdown("*Escrow status: Enabled*")
    else:
        st.warning("Lexi is still indexing the files... refresh shortly!")

# --- 3. SAFETY ---
elif menu == "🛡️ How Escrow Works":
    st.header("The Zimi Guarantee")
    st.image(ZIMI_SIDEBAR, width=150)
    st.write("ConfirmAm uses a secure Escrow system to make sure no one gets scammed.")
    
    st.markdown("""
    <div class="safety-card">
    <h4>1. Secure Payment</h4>
    <p>Captain Zimi holds your payment in a neutral vault. The seller only sees that the order is paid.</p>
    </div>
    <div class="safety-card">
    <h4>2. Verification</h4>
    <p>Merchant ships the product. Lexi monitors the tracking while you inspect the arrival.</p>
    </div>
    <div class="safety-card">
    <h4>3. Release</h4>
    <p>Money is only released to the seller after Zimi gets the 'All Clear' from you.</p>
    </div>
    """, unsafe_allow_html=True)

# --- 4. APPLY TO SELL ---
elif menu == "📥 Apply to Sell":
    st.markdown("### Become a Verified Merchant")
    st.info("Note: A 5% escrow commission applies to all successful sales on this platform.")
    
    with st.form("Merchant Application"):
        b_name = st.text_input("Business Name")
        b_niche = st.selectbox("Niche", ["Fashion", "Electronics", "Beauty", "Home", "Other"])
        b_email = st.text_input("Email Address")
        b_social = st.text_input("Instagram/TikTok Handle")
        b_phone = st.text_input("WhatsApp Number")
        
        submitted = st.form_submit_button("Submit Application")
        if submitted:
            if b_name and b_phone:
                st.success("Application started!")
                whatsapp_msg = f"Merchant%20App:%20{b_name}%0ANiche:%20{b_niche}"
                st.link_button("Finalize with Zimi", f"https://wa.me/{WHATSAPP_NUMBER}?text={whatsapp_msg}")

# --- 5. ADVERTISE PRODUCT ---
elif menu == "📢 Advertise Product":
    st.header("List Your Product")
    st.write("Submit your product details for review and listing in the mall.")
    
    st.warning("Merchant Notice: An administrative fee of 5% will be added to your base price upon listing.")
    
    with st.form("Product Ad Form"):
        p_name = st.text_input("Product Name")
        p_price = st.number_input("Your Asking Price (Base Price)", min_value=0)
        p_desc = st.text_area("Product Description")
        p_image = st.text_input("Image Link (URL)")
        p_vendor = st.text_input("Your Business Name")
        
        ad_submitted = st.form_submit_button("Submit Product for Review")
        
        if ad_submitted:
            if p_name and p_price > 0:
                st.success("Details ready! Click

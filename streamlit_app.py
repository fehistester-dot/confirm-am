import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="ConfirmAm Marketplace", 
    page_icon="https://i.postimg.cc/mD3WvH5n/Confirm-Am-Logo-Tick.png",
    layout="wide"
)

# 2. Assets & Links
FLUTTERWAVE_LINK = "https://flutterwave.com/pay/ctppxixgdke7"
LOGO_URL = "https://i.postimg.cc/mD3WvH5n/Confirm-Am-Logo-Tick.png"
SUPPORT_WA = "https://wa.me/2347046481507"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Amh_WmVwXCeZhc0h6NesZhBuGZAT0Ch60PuH-BF3xVE/export?format=csv"

# 3. Enhanced Styling
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .product-card {
        background-color: white;
        padding: 20px;
        border-radius: 20px;
        border: 1px solid #eee;
        margin-bottom: 25px;
        text-align: center;
        box-shadow: 0 10px 15px rgba(0,0,0,0.03);
    }
    .price-tag { color: #1DA1F2; font-weight: 900; font-size: 1.4em; }
    .verified-badge { color: #1DA1F2; font-size: 0.85em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.image(LOGO_URL, use_container_width=True)
st.sidebar.markdown("<h2 style='text-align:center;'>ConfirmAm</h2>", unsafe_allow_html=True)

st.sidebar.markdown("### 🛒 My Account")
if st.sidebar.button("📦 Track My Order", use_container_width=True):
    st.sidebar.info("Redirecting to Support...")
    st.sidebar.markdown(f'<meta http-equiv="refresh" content="0;url={SUPPORT_WA}?text=Hello%20ConfirmAm,%20I%20want%20to%20track%20my%20order">', unsafe_allow_html=True)

st.sidebar.markdown("---")
menu = st.sidebar.selectbox("Go to:", ["🛍️ Shopping Mall", "🛡️ How Escrow Works", "📥 Vendor Portal"])

# --- OPTION 1: SHOPPING MALL ---
if menu == "🛍️ Shopping Mall":
    st.markdown("<h1 style='text-align:center;'>ConfirmAm Mall</h1>", unsafe_allow_html=True)
    
    try:
        data = pd.read_csv(SHEET_URL)
        data.columns = data.columns.str.strip().str.lower()
        
        cols = st.columns(2)
        for i, row in data.iterrows():
            with cols[i % 2]:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                if 'image_url' in row and pd.notnull(row['image_url']):
                    st.image(row['image_url'], use_container_width=True)
                
                # Brand & Verified Logic
                is_v = str(row.get('verified', '')).strip().upper() == "TRUE"
                badge = '<span class="verified-badge">☑️ VERIFIED</span>' if is_v else ""
                
                st.markdown(f"""
                    <p style="margin:0; font-size:0.8em; color:#777;">{row.get('seller', 'Store')} {badge}</p>
                    <h3 style="margin:5px 0;">{row.get('name', 'Item')}</h3>
                    <p class="price-tag">₦{row.get('price', 0):,}</p>
                """, unsafe_allow_html=True)
                
                st.link_button("Secure Purchase", FLUTTERWAVE_LINK, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
    except:
        st.info("Catalog loading... Please refresh.")

# --- OPTION 2: HOW ESCROW WORKS ---
elif menu == "🛡️ How Escrow Works":
    st.title("The ConfirmAm Promise 🛡️")
    st.write("We hold the money so you don't get scammed.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 1. You Pay")
        st.write("Your money is held securely by ConfirmAm. The vendor cannot touch it yet.")
    with c2:
        st.markdown("### 2. Vendor Ships")
        st.write("We notify the vendor that payment is 'Locked.' They ship your item immediately.")
    with c3:
        st.markdown("### 3. You Confirm")
        st.write("Once you receive and check the item, you confirm. Only then do we pay the vendor.")
    
    st.success("Total Security. Zero Scams.")

# --- OPTION 3: VENDOR PORTAL ---
elif menu == "📥 Vendor Portal":
    st.title("Start Selling on ConfirmAm")
    st.write("Apply to become a verified 'Blue Tick' vendor.")
    with st.form("vendor_app"):
        st.text_input("Business Name")
        st.text_input("Instagram Handle")
        st.file_uploader("Upload ID (NIN/Drivers License)")
        if st.form_submit_button("Submit Application"):
            st.info("Our compliance team will reach out via WhatsApp.")

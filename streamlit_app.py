import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="ConfirmAm Marketplace", page_icon="🛡️", layout="wide")

# 2. THE DATABASE LINKS (Points to specific tabs)
SHEET_ID = "1-19BcEQqsLvRKoUX3opcah88GT6veC_8arPqryiJBWs"
# URL for the Products (Sheet1)
PRODUCTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Sheet1"
# URL for the Merchants (Sheet2/merchants)
MERCHANTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=merchants"

FLUTTERWAVE_LINK = "https://flutterwave.com/pay/ctppxixgdke7"

# 3. Design & Styling
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    .product-card, .merchant-card {
        background-color: white; padding: 15px; border-radius: 15px;
        border: 1px solid #eee; margin-bottom: 20px; text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .price-text { color: #1DA1F2; font-weight: 800; font-size: 1.3em; margin: 10px 0; }
    .verified-badge { color: #1DA1F2; font-size: 0.8em; font-weight: bold; border: 1px solid #1DA1F2; padding: 2px 5px; border-radius: 5px; }
    .hero-box { background: #1DA1F2; color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.image("https://i.postimg.cc/mD3WvH5n/Confirm-Am-Logo-Tick.png", use_container_width=True)
menu = st.sidebar.radio("Navigation", ["🛍️ Shopping Mall", "🛡️ Safety & Escrow", "🏢 Merchant Directory", "📥 Apply to Sell"])

# --- SHOPPING MALL ---
if menu == "🛍️ Shopping Mall":
    st.markdown('<div class="hero-box"><h1>ConfirmAm Mall</h1><p>Verified Items • Secure Escrow</p></div>', unsafe_allow_html=True)
    try:
        data = pd.read_csv(PRODUCTS_URL)
        data.columns = [c.strip().lower() for c in data.columns]
        items = data[data['status'].str.lower() == 'active']
        cols = st.columns(2)
        for i, row in items.iterrows():
            with cols[i % 2]:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                st.image(row.get('image_url', 'https://via.placeholder.com/300'), use_container_width=True)
                st.markdown(f"<b>{row.get('name', 'Item')}</b><p class='price-text'>₦{row.get('price', 0):,}</p>", unsafe_allow_html=True)
                st.link_button("Buy with Escrow", FLUTTERWAVE_LINK, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
    except:
        st.info("Loading inventory...")

# --- MERCHANT DIRECTORY (Manual Filling) ---
elif menu == "🏢 Merchant Directory":
    st.header("Our Verified Merchants")
    try:
        m_data = pd.read_csv(MERCHANTS_URL)
        m_data.columns = [c.strip().lower() for c in m_data.columns]
        for _, m in m_data.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="merchant-card">
                    <h3>{m.get('name')} {'☑️' if str(m.get('verified')).upper() == 'TRUE' else ''}</h3>
                    <p>Category: {m.get('category')} | Socials: {m.get('socials')}</p>
                </div>
                """, unsafe_allow_html=True)
    except:
        st.warning("No merchants listed yet. Add them to your 'merchants' tab in Google Sheets!")

# --- APPLY TO SELL (WhatsApp Direct) ---
elif menu == "📥 Apply to Sell":
    st.header("Join ConfirmAm")
    with st.form("Merchant Form"):
        biz_name = st.text_input("Business Name")
        biz_type = st.selectbox("Category", ["Fashion", "Electronics", "Beauty", "Other"])
        contact = st.text_input("WhatsApp Number")
        if st.form_submit_button("Submit"):
            wa_url = f"https://wa.me/2347046481507?text=Apply%20Business:%20{biz_name}"
            st.link_button("Finalize on WhatsApp", wa_url)

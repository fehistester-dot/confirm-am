import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="ConfirmAm Mall", page_icon="🛡️", layout="wide")

# 2. THE DATABASE (Using your new link)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-19BcEQqsLvRKoUX3opcah88GT6veC_8arPqryiJBWs/export?format=csv"
FLUTTERWAVE_LINK = "https://flutterwave.com/pay/ctppxixgdke7"

# 3. Design & Styling
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    .product-card {
        background-color: white; padding: 15px; border-radius: 15px;
        border: 1px solid #eee; margin-bottom: 20px; text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .price-text { color: #1DA1F2; font-weight: 800; font-size: 1.3em; margin: 10px 0; }
    .verified-badge { color: #1DA1F2; font-size: 0.8em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.image("https://i.postimg.cc/mD3WvH5n/Confirm-Am-Logo-Tick.png", use_container_width=True)
st.sidebar.markdown("<h2 style='text-align:center;'>ConfirmAm</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.subheader("📦 Order Status")
st.sidebar.link_button(
    "Track My Order", 
    "https://wa.me/2347046481507?text=Hello%20ConfirmAm,%20I%20just%20paid%20and%20need%20to%20track%20my%20order", 
    use_container_width=True,
    type="primary"
)
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigation", ["🛍️ Shopping Mall", "🛡️ Safety & Escrow"])

# --- SHOPPING MALL ---
if menu == "🛍️ Shopping Mall":
    st.markdown("<h1 style='text-align:center;'>ConfirmAm Mall</h1>", unsafe_allow_html=True)
    
    try:
        data = pd.read_csv(SHEET_URL)
        data.columns = [c.strip().lower() for c in data.columns]
        
        # Only show items where status is 'active'
        if 'status' in data.columns:
            data = data[data['status'].str.lower() == 'active']
        
        if data.empty:
            st.warning("The Mall is currently being stocked. Refresh in 1 minute!")
        else:
            cols = st.columns(2)
            for i, row in data.iterrows():
                with cols[i % 2]:
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    st.image(row.get('image_url', 'https://via.placeholder.com/300'), use_container_width=True)
                    
                    is_v = str(row.get('verified', '')).strip().upper() == "TRUE"
                    badge = '<span class="verified-badge">☑️ Verified</span>' if is_v else ""
                    
                    st.markdown(f"""
                        <p style="font-size:0.75em; color:#666; margin-bottom:2px;">{row.get('seller', 'ConfirmAm')} {badge}</p>
                        <b style="font-size:1.2em;">{row.get('name', 'Item')}</b>
                        <p class="price-text">₦{row.get('price', 0):,}</p>
                    """, unsafe_allow_html=True)
                    st.link_button("Buy with Escrow", FLUTTERWAVE_LINK, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error("Connecting to the database...")

elif menu == "🛡️ Safety & Escrow":
    st.title("Escrow Protection")
    st.write("We hold your money safely until you confirm delivery.")

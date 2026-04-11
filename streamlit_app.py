import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="ConfirmAm Marketplace", 
    page_icon="https://i.postimg.cc/mD3WvH5n/Confirm-Am-Logo-Tick.png",
    layout="wide"
)

# 2. YOUR UPDATED DATABASE & LINKS
# Linked to your new ConfirmAm_Database sheet
SHEET_ID = "1uQebi8rJgMpIfoXU7JfLcgb8ADa02R3DXoWzoDJC4Qo" 
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
FLUTTERWAVE_LINK = "https://flutterwave.com/pay/ctppxixgdke7"

# 3. Design & Styling
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    .product-card {
        background-color: white;
        padding: 15px;
        border-radius: 15px;
        border: 1px solid #eee;
        margin-bottom: 20px;
        text-align: center;
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
menu = st.sidebar.radio("Navigation", ["🛍️ Shopping Mall", "🛡️ Safety & Escrow", "📥 Merchant Portal"])

# --- SHOPPING MALL ---
if menu == "🛍️ Shopping Mall":
    st.markdown("<h1 style='text-align:center;'>ConfirmAm Mall</h1>", unsafe_allow_html=True)
    
    try:
        # Load and clean data
        data = pd.read_csv(SHEET_URL)
        data.columns = [c.strip().lower() for c in data.columns]
        
        # Filter for active items if the column exists
        if 'status' in data.columns:
            data = data[data['status'].str.lower() == 'active']
        
        if data.empty:
            st.warning("The Mall is currently refreshing. Check back in a moment!")
        else:
            cols = st.columns(2)
            for i, row in data.iterrows():
                with cols[i % 2]:
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    
                    # Display product image
                    img = row.get('image_url', 'https://via.placeholder.com/300')
                    st.image(img, use_container_width=True)
                    
                    # Verified Branding
                    is_v = str(row.get('verified', '')).strip().upper() == "TRUE"
                    badge = '<span class="verified-badge">☑️ Verified</span>' if is_v else ""
                    
                    st.markdown(f"""
                        <p style="font-size:0.75em; color:#666; margin-bottom:2px;">{row.get('seller', 'Vendor')} {badge}</p>
                        <b style="font-size:1.2em;">{row.get('name', 'Item')}</b>
                        <p class="price-text">₦{row.get('price', 0):,}</p>
                    """, unsafe_allow_html=True)
                    
                    st.link_button("Buy with Escrow", FLUTTERWAVE_LINK, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error("Setting up the connection... Please ensure your Google Sheet is shared as 'Anyone with the link'.")

# --- OTHER SECTIONS ---
elif menu == "🛡️ Safety & Escrow":
    st.title("How ConfirmAm Protects You")
    st.write("Safe. Secure. Vetted.")
    # (Existing Escrow Logic)

elif menu == "📥 Merchant Portal":
    st.title("Partner with ConfirmAm")
    # (Existing Portal Logic)

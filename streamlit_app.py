import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="ConfirmAm Marketplace", 
    page_icon="https://i.postimg.cc/mD3WvH5n/Confirm-Am-Logo-Tick.png",
    layout="wide"
)

# 2. THE DATABASE & LINKS
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-19BcEQqsLvRKoUX3opcah88GT6veC_8arPqryiJBWs/export?format=csv"
FLUTTERWAVE_LINK = "https://flutterwave.com/pay/ctppxixgdke7"

# 3. Enhanced Design & Styling
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    .product-card {
        background-color: white; padding: 15px; border-radius: 15px;
        border: 1px solid #eee; margin-bottom: 20px; text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .price-text { color: #1DA1F2; font-weight: 800; font-size: 1.3em; margin: 10px 0; }
    .verified-badge { color: #1DA1F2; font-size: 0.8em; font-weight: bold; border: 1px solid #1DA1F2; padding: 2px 5px; border-radius: 5px; }
    .hero-box { background: #1DA1F2; color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 25px; }
    .trust-bar { background-color: #e1f5fe; padding: 10px; border-radius: 10px; text-align: center; margin-bottom: 20px; border: 1px dashed #01579b; }
    .delivery-tag { font-size: 0.8em; color: #2e7d32; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.image("https://i.postimg.cc/mD3WvH5n/Confirm-Am-Logo-Tick.png", use_container_width=True)
st.sidebar.markdown("<h2 style='text-align:center;'>ConfirmAm</h2>", unsafe_allow_html=True)

# Currency Switcher
st.sidebar.markdown("---")
st.sidebar.subheader("🌍 International Pricing")
currency = st.sidebar.selectbox("Select Currency", ["NGN (₦)", "USD ($)"])
exchange_rate = 1600 

st.sidebar.markdown("---")
st.sidebar.subheader("📦 Customer Service")
st.sidebar.link_button("Track My Order", "https://wa.me/2347046481507?text=Hello%20ConfirmAm,%20I%20just%20paid%20and%20need%20to%20send%20my%20address", use_container_width=True, type="primary")

menu = st.sidebar.radio("Navigation", ["🛍️ Shopping Mall", "🛡️ Safety & Escrow", "📥 Merchant Portal"])

# --- DATA LOADING ---
@st.cache_data(ttl=10)
def get_fresh_data(url):
    df = pd.read_csv(url)
    df.columns = [c.strip().lower() for c in df.columns]
    return df

# --- SHOPPING MALL ---
if menu == "🛍️ Shopping Mall":
    st.markdown('<div class="hero-box"><h1>ConfirmAm Mall</h1><p>Verified Items • Secure Escrow • Fast Delivery</p></div>', unsafe_allow_html=True)
    
    try:
        data = get_fresh_data(SHEET_URL)
        search_query = st.text_input("🔍 Search products...", "")
        
        if 'status' in data.columns:
            data = data[data['status'].str.lower() == 'active']
        
        # Featured Section
        if 'featured' in data.columns and not search_query:
            featured_items = data[data['featured'].str.lower() == 'yes']
            if not featured_items.empty:
                st.subheader("✨ Featured Arrivals")
                f_cols = st.columns(len(featured_items))
                for idx, (f_idx, f_row) in enumerate(featured_items.iterrows()):
                    with f_cols[idx]:
                        st.image(f_row.get('image_url', 'https://via.placeholder.com/150'), use_container_width=True)
                        st.caption(f"**{f_row.get('name')}**")

        st.markdown("---")
        
        cols = st.columns(2)
        for i, row in data.iterrows():
            with cols[i % 2]:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                st.image(row.get('image_url', 'https://via.placeholder.com/300'), use_container_width=True)
                
                naira_price = row.get('price', 0)
                display_price = f"${(naira_price / exchange_rate):,.2f}" if currency == "USD ($)" else f"₦{naira_price:,}"
                
                st.markdown(f"""
                    <b style="font-size:1.1em; display:block; height:40px;">{row.get('name', 'Item')}</b>
                    <p class="price-text">{display_price}</p>
                """, unsafe_allow_html=True)
                
                # UPDATED BUTTON TEXT
                st.link_button("Buy with ConfirmAm Escrow", FLUTTERWAVE_LINK, use_container_width=True)
                
                if st.button(f"Generate Receipt: {row.get('name')[:10]}", key=f"btn_{i}"):
                    st.code(f"CONFIRMAM RECEIPT\nITEM: {row.get('name')}\nPRICE: {display_price}\nSTATUS: AWAITING PAYMENT", language="markdown")
                
                st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error("Connecting...")

# --- SAFETY & ESCROW ---
elif menu == "🛡️ Safety & Escrow":
    st.markdown("<h1 style='text-align:center;'>Safe Payment Guide</h1>", unsafe_allow_html=True)
    
    st.info("""
    💡 **Paying via Bank Transfer?**
    When you choose 'Bank Transfer' on our payment page, Flutterwave will generate a unique account number for your order. 
    **Don't worry if you see 'ConfirmAm' or your name on the account destination—this is a secure virtual account created just for your transaction.**
    """)
    
    st.markdown("""
    ### 🛡️ The ConfirmAm Guarantee:
    1. **You Pay:** Funds are held by us.
    2. **We Verify:** We ensure the vendor is ready to ship.
    3. **You Receive:** You get your item and confirm it's what you ordered.
    4. **We Release:** Only then is the seller paid.
    """)

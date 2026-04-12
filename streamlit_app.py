import streamlit as st
import pandas as pd

# 1. Page Configuration (STAYS THE SAME)
st.set_page_config(
    page_title="ConfirmAm Marketplace", 
    page_icon="https://i.postimg.cc/mD3WvH5n/Confirm-Am-Logo-Tick.png",
    layout="wide"
)

# 2. THE DATABASE & LINKS (STAYS THE SAME)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-19BcEQqsLvRKoUX3opcah88GT6veC_8arPqryiJBWs/export?format=csv"
FLUTTERWAVE_LINK = "https://flutterwave.com/pay/ctppxixgdke7"

# ZIMI LINKS
ZIMI_WAVING = "https://i.postimg.cc/9QdS9nRv/Gemini-Generated-Image-5wc5485wc5485wc5-removebg-preview.png"
ZIMI_THINKING = "https://i.postimg.cc/ZKyXbRJ1/Gemini-Generated-Image-5wc5485wc5485wc5-2-removebg-preview.png"
ZIMI_HAPPY = "https://i.postimg.cc/7h5dTP0K/Gemini-Generated-Image-5wc5485wc5485wc5-1-removebg-preview.png"

# 3. Zimi Mood Logic (New, but non-intrusive)
if 'zimi_mood' not in st.session_state:
    st.session_state.zimi_mood = ZIMI_WAVING

# 4. Styling (INCLUDING THE ORIGINAL STYLES + NEW ZIMI FLOAT)
st.markdown(f"""
    <style>
    .stApp {{ background-color: #fcfcfc; }}
    .product-card {{
        background-color: white; padding: 15px; border-radius: 15px;
        border: 1px solid #eee; margin-bottom: 20px; text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }}
    .price-text {{ color: #1DA1F2; font-weight: 800; font-size: 1.3em; margin: 10px 0; }}
    .hero-box {{ background: #1DA1F2; color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 25px; }}
    
    .zimi-float {{
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1000;
        width: 120px;
        filter: drop-shadow(0px 10px 15px rgba(0,0,0,0.2));
    }}
    </style>
    
    <div class="zimi-float">
        <img src="{st.session_state.zimi_mood}" width="100%">
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR (RESTORED TO ORIGINAL) ---
st.sidebar.image("https://i.postimg.cc/mD3WvH5n/Confirm-Am-Logo-Tick.png", use_container_width=True)
st.sidebar.markdown("<h2 style='text-align:center;'>ConfirmAm</h2>", unsafe_allow_html=True)

# Currency Switcher (RESTORED)
st.sidebar.markdown("---")
st.sidebar.subheader("🌍 International Pricing")
currency = st.sidebar.selectbox("Select Currency", ["NGN (₦)", "USD ($)"])
exchange_rate = 1600 

st.sidebar.markdown("---")
st.sidebar.subheader("📦 Customer Service")
st.sidebar.link_button("Track My Order", "https://wa.me/2347046481507?text=Hello%20ConfirmAm...", use_container_width=True, type="primary")

menu = st.sidebar.radio("Navigation", ["🛍️ Shopping Mall", "🛡️ Safety & Escrow", "📥 Merchant Portal"])

# Zimi reacts to navigation
if menu == "🛍️ Shopping Mall":
    st.session_state.zimi_mood = ZIMI_WAVING
elif menu == "🛡️ Safety & Escrow":
    st.session_state.zimi_mood = ZIMI_THINKING

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
        
        cols = st.columns(2)
        for i, row in data.iterrows():
            with cols[i % 2]:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                st.image(row.get('image_url', 'https://via.placeholder.com/300'), use_container_width=True)
                
                naira_price = row.get('price', 0)
                display_price = f"${(naira_price / exchange_rate):,.2f}" if currency == "USD ($)" else f"₦{naira_price:,}"
                
                st.markdown(f"<b>{row.get('name', 'Item')}</b><p class='price-text'>{display_price}</p>", unsafe_allow_html=True)
                
                # RESTORED BUTTON TEXT
                st.link_button("Buy with ConfirmAm Escrow", FLUTTERWAVE_LINK, use_container_width=True)
                
                if st.button(f"Generate Receipt: {row.get('name')[:10]}", key=f"btn_{i}"):
                    st.session_state.zimi_mood = ZIMI_HAPPY
                    st.balloons()
                    st.code(f"CONFIRMAM RECEIPT\nITEM: {row.get('name')}\nPRICE: {display_price}\nSTATUS: AWAITING PAYMENT", language="markdown")
                
                st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error("Connecting...")

# --- SAFETY & ESCROW (RESTORED) ---
elif menu == "🛡️ Safety & Escrow":
    st.markdown("<h1 style='text-align:center;'>Zimi's Safety Guide</h1>", unsafe_allow_html=True)
    st.info("💡 **Zimi says:** 'Don't worry about bank transfers! Flutterwave creates a unique account just for you under our name.'")
    
    st.markdown("""
    ### 🛡️ Why use ConfirmAm Escrow?
    * **Anti-Scam:** We hold the money, not the seller.
    * **Quality Check:** You verify the item before we release funds.
    """)

import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="ConfirmAm Marketplace", 
    page_icon="https://i.postimg.cc/mD3WvH5n/Confirm-Am-Logo-Tick.png",
    layout="wide"
)

# 2. ASSETS & DATABASE
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-19BcEQqsLvRKoUX3opcah88GT6veC_8arPqryiJBWs/export?format=csv"
FLUTTERWAVE_LINK = "https://flutterwave.com/pay/ctppxixgdke7"

# ZIMI LINKS
ZIMI_WAVING = "https://i.postimg.cc/9QdS9nRv/Gemini-Generated-Image-5wc5485wc5485wc5-removebg-preview.png"
ZIMI_THINKING = "https://i.postimg.cc/ZKyXbRJ1/Gemini-Generated-Image-5wc5485wc5485wc5-2-removebg-preview.png"
ZIMI_HAPPY = "https://i.postimg.cc/7h5dTP0K/Gemini-Generated-Image-5wc5485wc5485wc5-1-removebg-preview.png"

# 3. Session State
if 'zimi_mood' not in st.session_state:
    st.session_state.zimi_mood = ZIMI_WAVING

# 4. Styling (Floating Zimi + Original Colors)
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

# --- SIDEBAR ---
st.sidebar.image("https://i.postimg.cc/mD3WvH5n/Confirm-Am-Logo-Tick.png", use_container_width=True)
st.sidebar.markdown("<h2 style='text-align:center;'>ConfirmAm</h2>", unsafe_allow_html=True)

st.sidebar.markdown("---")
currency = st.sidebar.selectbox("Select Currency", ["NGN (₦)", "USD ($)"])
exchange_rate = 1600 

st.sidebar.markdown("---")
st.sidebar.link_button("Track My Order", "https://wa.me/2347046481507", use_container_width=True)

menu = st.sidebar.radio("Navigation", ["🛍️ Shopping Mall", "🛡️ Safety & Escrow", "📥 Merchant Portal"])

# --- PAGE LOGIC ---

if menu == "🛍️ Shopping Mall":
    st.session_state.zimi_mood = ZIMI_WAVING
    st.markdown('<div class="hero-box"><h1>ConfirmAm Mall</h1><p>Verified Items • Secure Escrow</p></div>', unsafe_allow_html=True)
    
    # [Original Shopping Mall Data Logic here...]
    try:
        data = pd.read_csv(SHEET_URL)
        data.columns = [c.strip().lower() for c in data.columns]
        cols = st.columns(2)
        for i, row in data.iterrows():
            with cols[i % 2]:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                st.image(row.get('image_url', 'https://via.placeholder.com/300'), use_container_width=True)
                n_p = row.get('price', 0)
                p_text = f"${(n_p/1600):,.2f}" if currency == "USD ($)" else f"₦{n_p:,}"
                st.markdown(f"<b>{row.get('name')}</b><p class='price-text'>{p_text}</p>", unsafe_allow_html=True)
                st.link_button("Buy with ConfirmAm Escrow", FLUTTERWAVE_LINK, use_container_width=True)
                if st.button(f"Generate Receipt: {i}", key=f"r_{i}"):
                    st.session_state.zimi_mood = ZIMI_HAPPY
                    st.balloons()
                    st.code(f"CONFIRMAM RECEIPT\nITEM: {row.get('name')}\nPRICE: {p_text}")
                st.markdown('</div>', unsafe_allow_html=True)
    except: st.error("Refreshing...")

elif menu == "🛡️ Safety & Escrow":
    st.session_state.zimi_mood = ZIMI_THINKING
    st.markdown("<h1 style='text-align:center;'>Safety Guide</h1>", unsafe_allow_html=True)
    st.info("Zimi is watching the vault! Funds are held until delivery is confirmed.")

elif menu == "📥 Merchant Portal":
    st.session_state.zimi_mood = ZIMI_WAVING
    st.markdown("<h1 style='text-align:center;'>Partner with ConfirmAm</h1>", unsafe_allow_html=True)
    
    # THE INTERNAL FORM (No links!)
    with st.form("merchant_registration"):
        st.subheader("Business Registration")
        biz_name = st.text_input("Business Name")
        contact_person = st.text_input("Contact Person Name")
        whatsapp = st.text_input("WhatsApp Number")
        category = st.selectbox("What do you sell?", ["Fashion", "Electronics", "Groceries", "Other"])
        
        submitted = st.form_submit_button("Submit Application")
        
        if submitted:
            if biz_name and whatsapp:
                st.session_state.zimi_mood = ZIMI_HAPPY
                st.success(f"Oshey! {biz_name} application received. Zimi is reviewing it now!")
                st.balloons()
            else:
                st.error("Please fill in your Business Name and WhatsApp.")

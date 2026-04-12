import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="ConfirmAm Marketplace", 
    page_icon="https://cdn-icons-png.flaticon.com/512/1162/1162456.png",
    layout="wide"
)

# 2. ASSETS
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-19BcEQqsLvRKoUX3opcah88GT6veC_8arPqryiJBWs/export?format=csv"
FLUTTERWAVE_LINK = "https://flutterwave.com/pay/ctppxixgdke7"
MY_WHATSAPP = "2347046481507" # Your number is already locked in

# ZIMI LINKS
ZIMI_WAVING = "https://i.postimg.cc/9QdS9nRv/Gemini-Generated-Image-5wc5485wc5485wc5-removebg-preview.png"
ZIMI_THINKING = "https://i.postimg.cc/ZKyXbRJ1/Gemini-Generated-Image-5wc5485wc5485wc5-2-removebg-preview.png"
ZIMI_HAPPY = "https://i.postimg.cc/7h5dTP0K/Gemini-Generated-Image-5wc5485wc5485wc5-1-removebg-preview.png"

# 3. Session State
if 'zimi_mood' not in st.session_state:
    st.session_state.zimi_mood = ZIMI_WAVING

# 4. Global Styling (LOCKING THE DESIGN)
st.markdown(f"""
    <style>
    .stApp {{ background-color: #fcfcfc; }}
    .product-card {{
        background-color: white; padding: 8px; border-radius: 10px;
        border: 1px solid #eee; margin-bottom: 10px; text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    .price-text {{ color: #1DA1F2; font-weight: 800; font-size: 1.0em; margin: 3px 0; }}
    .hero-box {{ background: #1DA1F2; color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 25px; }}
    
    .zimi-float {{
        position: fixed;
        bottom: -20px; right: -50px; z-index: 9999;
        width: 390px; pointer-events: none;
        transition: all 0.4s ease-in-out;
    }}
    </style>
    <div class="zimi-float"><img src="{st.session_state.zimi_mood}" width="100%"></div>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.markdown(f"<div style='text-align: center;'><img src='https://cdn-icons-png.flaticon.com/512/1162/1162456.png' width='80'></div>", unsafe_allow_html=True)
st.sidebar.markdown("<h2 style='text-align:center;'>ConfirmAm</h2>", unsafe_allow_html=True)
currency = st.sidebar.selectbox("Select Currency", ["NGN (₦)", "USD ($)"])
exchange_rate = 1600 

menu = st.sidebar.radio("Navigation", ["🛍️ Shopping Mall", "🛡️ Safety & Escrow", "📥 Merchant Portal"])

# --- PAGE LOGIC ---

if menu == "🛍️ Shopping Mall":
    st.session_state.zimi_mood = ZIMI_WAVING
    st.markdown('<div class="hero-box"><h1>ConfirmAm Mall</h1><p>Verified Items • Secure Escrow • 10% Protection Fee Included</p></div>', unsafe_allow_html=True)
    try:
        data = pd.read_csv(SHEET_URL)
        data.columns = [c.strip().lower() for c in data.columns]
        cols = st.columns(5) 
        for i, row in data.iterrows():
            with cols[i % 5]:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                st.image(row.get('image_url', 'https://via.placeholder.com/150'), use_container_width=True)
                total = row.get('price', 0) * 1.10
                price_display = f"${(total/exchange_rate):,.2f}" if currency == "USD ($)" else f"₦{total:,.0f}"
                st.markdown(f"<p style='font-size:0.8em; margin:0;'>{row.get('name')[:20]}</p><p class='price-text'>{price_display}</p>", unsafe_allow_html=True)
                st.link_button("Buy", FLUTTERWAVE_LINK, use_container_width=True)
                if st.button(f"Receipt", key=f"r_{i}"):
                    st.session_state.zimi_mood = ZIMI_HAPPY
                    st.balloons()
                st.markdown('</div>', unsafe_allow_html=True)
    except: st.error("Refreshing...")

elif menu == "🛡️ Safety & Escrow":
    st.session_state.zimi_mood = ZIMI_THINKING
    st.markdown("<h1 style='text-align:center;'>🛡️ Safety Vault</h1>", unsafe_allow_html=True)

elif menu == "📥 Merchant Portal":
    st.session_state.zimi_mood = ZIMI_WAVING
    st.markdown("<h1 style='text-align:center;'>Partner with ConfirmAm</h1>", unsafe_allow_html=True)
    
    with st.form("merchant_whatsapp_form"):
        biz_name = st.text_input("Business Name")
        contact = st.text_input("Contact Person Name")
        wa_num = st.text_input("WhatsApp Number")
        cat = st.selectbox("Category", ["Fashion", "Electronics", "Groceries", "Other"])
        
        submitted = st.form_submit_button("Generate Application Message")
        
        if submitted:
            if biz_name and wa_num:
                # Pre-fills a WhatsApp message
                msg = f"Hello ConfirmAm! I want to join as a Merchant.%0A%0A*Business:* {biz_name}%0A*Contact:* {contact}%0A*WhatsApp:* {wa_num}%0A*Category:* {cat}"
                wa_url = f"https://wa.me/{MY_WHATSAPP}?text={msg}"
                
                st.session_state.zimi_mood = ZIMI_HAPPY
                st.success("Oshey! Click the button below to send your application to Zimi via WhatsApp.")
                st.link_button("🚀 Send Application via WhatsApp", wa_url, use_container_width=True)
                st.balloons()
            else:
                st.error("Please fill Business Name and WhatsApp.")

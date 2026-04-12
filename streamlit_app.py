import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="ConfirmAm Marketplace", 
    page_icon="https://cdn-icons-png.flaticon.com/512/1162/1162456.png",
    layout="wide"
)

# 2. ASSETS & DATABASE
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-19BcEQqsLvRKoUX3opcah88GT6veC_8arPqryiJBWs/export?format=csv"
FLUTTERWAVE_LINK = "https://flutterwave.com/pay/ctppxixgdke7"
MY_WHATSAPP = "2347046481507" 

# ZIMI MOODS
ZIMI_WAVING = "https://i.postimg.cc/9QdS9nRv/Gemini-Generated-Image-5wc5485wc5485wc5-removebg-preview.png"
ZIMI_THINKING = "https://i.postimg.cc/ZKyXbRJ1/Gemini-Generated-Image-5wc5485wc5485wc5-2-removebg-preview.png"
ZIMI_HAPPY = "https://i.postimg.cc/7h5dTP0K/Gemini-Generated-Image-5wc5485wc5485wc5-1-removebg-preview.png"

# 3. Session State
if 'zimi_mood' not in st.session_state:
    st.session_state.zimi_mood = ZIMI_WAVING

# 4. Global Styling (THE CONFIRM-AM DESIGN SYSTEM)
st.markdown(f"""
    <style>
    .stApp {{ background-color: #fcfcfc; }}
    .product-card {{
        background-color: white; padding: 10px; border-radius: 12px;
        border: 1px solid #eee; margin-bottom: 15px; text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }}
    .price-text {{ color: #1DA1F2; font-weight: 800; font-size: 1.1em; margin: 5px 0; }}
    .hero-box {{ background: #1DA1F2; color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 25px; }}
    
    .zimi-float {{
        position: fixed;
        bottom: -20px; right: -50px; z-index: 9999;
        width: 390px; pointer-events: none;
        transition: all 0.4s ease-in-out;
    }}

    .safety-card {{
        background: linear-gradient(135deg, #1DA1F2 0%, #0d8bd9 100%);
        color: white; padding: 30px; border-radius: 20px;
        display: flex; align-items: center; margin-top: 20px;
    }}
    </style>
    <div class="zimi-float"><img src="{st.session_state.zimi_mood}" width="100%"></div>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.markdown(f"<div style='text-align: center;'><img src='https://cdn-icons-png.flaticon.com/512/1162/1162456.png' width='80'></div>", unsafe_allow_html=True)
st.sidebar.markdown("<h2 style='text-align:center;'>ConfirmAm</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")
currency = st.sidebar.selectbox("Select Currency", ["NGN (₦)", "USD ($)"])
exchange_rate = 1600 
st.sidebar.markdown("---")
st.sidebar.link_button("Track My Order", f"https://wa.me/{MY_WHATSAPP}", use_container_width=True)

menu = st.sidebar.radio("Navigation", ["🛍️ Shopping Mall", "🛡️ Safety & Escrow", "📥 Merchant Portal"])

# --- PAGE LOGIC ---

if menu == "🛍️ Shopping Mall":
    st.session_state.zimi_mood = ZIMI_WAVING
    st.markdown('<div class="hero-box"><h1>ConfirmAm Mall</h1><p>Verified Items • Secure Escrow • 10% Protection Fee Included</p></div>', unsafe_allow_html=True)
    try:
        data = pd.read_csv(SHEET_URL)
        data.columns = [c.strip().lower() for c in data.columns]
        cols = st.columns(5) # 5-Column Sleek Grid
        for i, row in data.iterrows():
            with cols[i % 5]:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                st.image(row.get('image_url', 'https://via.placeholder.com/150'), use_container_width=True)
                
                base_price = row.get('price', 0)
                total = base_price * 1.10
                
                price_display = f"${(total/exchange_rate):,.2f}" if currency == "USD ($)" else f"₦{total:,.0f}"
                
                st.markdown(f"<p style='font-size:0.9em; margin:0;'><b>{row.get('name')[:20]}</b></p><p class='price-text'>{price_display}</p>", unsafe_allow_html=True)
                st.link_button("Buy", FLUTTERWAVE_LINK, use_container_width=True)
                
                if st.button(f"Receipt", key=f"r_{i}"):
                    st.session_state.zimi_mood = ZIMI_HAPPY
                    st.balloons()
                st.markdown('</div>', unsafe_allow_html=True)
    except: st.error("Refreshing inventory...")

elif menu == "🛡️ Safety & Escrow":
    st.session_state.zimi_mood = ZIMI_THINKING
    st.markdown("<h1 style='text-align:center;'>🛡️ ConfirmAm Safety Vault</h1>", unsafe_allow_html=True)
    
    # RESTORED SAFETY CONTENT
    st.markdown("""
    <div class="safety-card">
        <div style="flex: 1;">
            <h2 style="color: white; margin-bottom: 10px;">Your Funds are 100% Protected</h2>
            <p style="font-size: 1.1em; opacity: 0.9;">We hold your payment in our secure escrow vault. The seller only gets paid after you confirm you've received exactly what you ordered.</p>
        </div>
        <div style="flex: 0.4; text-align: right;">
            <img src="https://cdn-icons-png.flaticon.com/512/3596/3596091.png" width="140px">
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.info("💡 **Zimi's Tip:** 'Shop with confidence. If the seller doesn't deliver, we refund you immediately!'")

elif menu == "📥 Merchant Portal":
    st.session_state.zimi_mood = ZIMI_WAVING
    st.markdown("<h1 style='text-align:center;'>Partner with ConfirmAm</h1>", unsafe_allow_html=True)
    
    with st.form("merchant_wa_form"):
        biz_name = st.text_input("Business Name")
        contact = st.text_input("Contact Person Name")
        wa_num = st.text_input("WhatsApp Number")
        cat = st.selectbox("Category", ["Fashion", "Electronics", "Groceries", "Other"])
        
        submitted = st.form_submit_button("Generate Application Message")
        
        if submitted:
            if biz_name and wa_num:
                msg = f"Hello ConfirmAm! I want to join as a Merchant.%0A%0A*Business:* {biz_name}%0A*Contact:* {contact}%0A*WhatsApp:* {wa_num}%0A*Category:* {cat}"
                st.session_state.zimi_mood = ZIMI_HAPPY
                st.success("

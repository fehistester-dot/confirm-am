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

# 4. Global Styling
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
    .featured-box {{ background: #FFF9E6; border: 2px solid #FFD700; padding: 15px; border-radius: 15px; margin-bottom: 20px; }}
    
    .zimi-float {{
        position: fixed;
        bottom: -20px; 
        right: -50px; 
        z-index: 9999;
        width: 390px;
        filter: drop-shadow(0px 10px 15px rgba(0,0,0,0.2));
        pointer-events: none;
        transition: all 0.4s ease-in-out;
    }}

    /* THE ATM CARD SECTION STYLING */
    .safety-card {{
        background: linear-gradient(135deg, #1DA1F2 0%, #0d8bd9 100%);
        color: white;
        padding: 30px;
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 20px;
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

# Update Zimi based on menu
if menu == "🛡️ Safety & Escrow":
    st.session_state.zimi_mood = ZIMI_THINKING
else:
    st.session_state.zimi_mood = ZIMI_WAVING

# --- PAGE LOGIC ---

if menu == "🛍️ Shopping Mall":
    st.markdown('<div class="hero-box"><h1>ConfirmAm Mall</h1><p>Verified Items • Secure Escrow • 10% Fee Included</p></div>', unsafe_allow_html=True)
    try:
        data = pd.read_csv(SHEET_URL)
        data.columns = [c.strip().lower() for c in data.columns]
        search_query = st.text_input("🔍 Search products...", "").lower()
        if not search_query:
            st.markdown('<div class="featured-box"><b>🌟 Zimi Pick:</b> Highly rated vendor.</div>', unsafe_allow_html=True)
            feat = data.iloc[0]
            st.info(f"Top Choice Today: {feat.get('name', 'Premium Choice')}")
        filtered_data = data[data['name'].str.contains(search_query, na=False)] if search_query else data
        cols = st.columns(5) 
        for i, row in filtered_data.iterrows():
            with cols[i % 5]:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                st.image(row.get('image_url', 'https://via.placeholder.com/300'), use_container_width=True)
                base_price = row.get('price', 0)
                commission = base_price * 0.10
                total_naira = base_price + commission
                if currency == "USD ($)":
                    display_price = f"${(total_naira / exchange_rate):,.2f}"
                else:
                    display_price = f"₦{total_naira:,}"
                st.markdown(f"<p style='font-size:0.8em; margin:0;'>{row.get('name')[:20]}</p><p class='price-text'>{display_price}</p>", unsafe_allow_html=True)
                st.link_button("Buy", FLUTTERWAVE_LINK, use_container_width=True)
                if st.button(f"Receipt", key=f"r_{i}"):
                    st.session_state.zimi_mood = ZIMI_HAPPY
                    st.balloons()
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    except: st.error("Refreshing...")

elif menu == "🛡️ Safety & Escrow":
    st.markdown("<h1 style='text-align:center;'>🛡️ ConfirmAm Safety Vault</h1>", unsafe_allow_html=True)
    
    # THE RESTORED ATM CARD SECTION
    st.markdown("""
    <div class="safety-card">
        <div style="flex: 1;">
            <h2 style="color: white; margin-bottom: 10px;">Your Funds are 100% Protected</h2>
            <p style="font-size: 1.1em; opacity: 0.9;">We hold your payment in our secure escrow vault. The seller only gets paid after you confirm you've received exactly what you ordered. No long stories!</p>
        </div>
        <div style="flex: 0.5; text-align: right;">
            <img src="https://i.postimg.cc/vH2X7h7z/atm-hand.png" width="180px" style="filter: drop-shadow(5px 5px 10px rgba(0,0,0,0.3));">
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.info("💡 **Zimi's Tip:** 'If it's not what you ordered, don't worry. We handle the refund so you don't have to chase the seller!'")
    
    st.markdown("""
    ### 🛡️ Why use ConfirmAm Escrow?
    * **Anti-Scam:** We hold the money, not the seller. No pay, no loss!
    * **Quality Check:** You verify the item before we release your hard-earned funds.
    * **No Stress:** If the item never arrives or it's "wash," you get your money back instantly.
    * **Verified Sellers:** We only partner with merchants who pass Zimi's style and trust test.
    """)

elif menu == "📥 Merchant Portal":
    st.markdown("<h1 style='text-align:center;'>Partner with ConfirmAm</h1>", unsafe_allow_html=True)
    with st.form("merchant_registration_full"):
        st.subheader("Business Registration")
        biz_name = st.text_input("Business Name")
        contact_person = st.text_input("Contact Person Name")
        whatsapp = st.text_input("WhatsApp Number")
        category = st.selectbox("What do you sell?", ["Fashion", "Electronics", "Groceries", "Other"])
        submitted = st.form_submit_button("Submit Application")
        if submitted and biz_name:
            st.session_state.zimi_mood = ZIMI_HAPPY
            st.success(f"Oshey! {biz_name} application received. Zimi is reviewing it now!")
            st.balloons()
            st.rerun()

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
    
    /* SMALLER PRODUCT CARDS */
    .product-card {{
        background-color: white; 
        padding: 10px; 
        border-radius: 12px;
        border: 1px solid #eee; 
        margin-bottom: 15px; 
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    .price-text {{ color: #1DA1F2; font-weight: 800; font-size: 1.1em; margin: 5px 0; }}
    .hero-box {{ background: #1DA1F2; color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 25px; }}
    .featured-box {{ background: #FFF9E6; border: 2px solid #FFD700; padding: 15px; border-radius: 15px; margin-bottom: 20px; }}
    
    /* THE LARGE SIDE ZIMI */
    .zimi-float {{
        position: fixed;
        bottom: -20px; /* Anchored slightly lower for a better look */
        right: -50px; /* Pushed slightly off-side so she doesn't block the center */
        z-index: 9999;
        width: 390px;
        filter: drop-shadow(0px 10px 15px rgba(0,0,0,0.2));
        pointer-events: none; /* Allows user to click buttons BEHIND Zimi */
        transition: all 0.5s ease-in-out;
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
st.sidebar.subheader("🌍 International Pricing")
currency = st.sidebar.selectbox("Select Currency", ["NGN (₦)", "USD ($)"])
exchange_rate = 1600 

st.sidebar.markdown("---")
st.sidebar.subheader("📦 Support")
st.sidebar.link_button("Track My Order", "https://wa.me/2347046481507", use_container_width=True)

menu = st.sidebar.radio("Navigation", ["🛍️ Shopping Mall", "🛡️ Safety & Escrow", "📥 Merchant Portal"])

# --- PAGE LOGIC ---

if menu == "🛍️ Shopping Mall":
    st.session_state.zimi_mood = ZIMI_WAVING
    st.markdown('<div class="hero-box"><h1>ConfirmAm Mall</h1><p>Verified Items • Secure Escrow • 10% Protection Fee Included</p></div>', unsafe_allow_html=True)
    
    try:
        data = pd.read_csv(SHEET_URL)
        data.columns = [c.strip().lower() for c in data.columns]

        search_query = st.text_input("🔍 Search products...", "").lower()
        
        if not search_query:
            st.markdown('<div class="featured-box"><b>🌟 Zimi\'s Pick:</b> Highly rated vendor.</div>', unsafe_allow_html=True)
            feat = data.iloc[0]
            st.info(f"Top Choice Today: {feat.get('name', 'Premium Choice')}")

        filtered_data = data[data['name'].str.contains(search_query, na=False)] if search_query else data

        # 3-COLUMN GRID FOR SMALLER ITEMS
        cols = st.columns(3) 
        for i, row in filtered_data.iterrows():
            with cols[i % 3]:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                st.image(row.get('image_url', 'https://via.placeholder.com/300'), use_container_width=True)
                
                # COMMISSION LOGIC
                base_price = row.get('price', 0)
                commission = base_price * 0.10
                total_naira = base_price + commission
                
                if currency == "USD ($)":
                    display_price = f"${(total_naira / exchange_rate):,.2f}"
                    comm_text = f"${(commission / exchange_rate):,.2f}"
                else:
                    display_price = f"₦{total_naira:,}"
                    comm_text = f"₦{commission:,}"
                
                st.markdown(f"<small>{row.get('name')}</small><p class='price-text'>{display_price}</p>", unsafe_allow_html=True)
                st.link_button("Buy Now", FLUTTERWAVE_LINK, use_container_width=True)
                
                if st.button(f"Receipt", key=f"r_{i}"):
                    st.session_state.zimi_mood = ZIMI_HAPPY
                    st.balloons()
                    st.code(f"CONFIRMAM RECEIPT\nITEM: {row.get('name')}\nSELLER PRICE: {base_price:,}\nESCROW FEE (10%): {comm_text}\nTOTAL: {display_price}")
                st.markdown('</div>', unsafe_allow_html=True)
    except: st.error("Refreshing Mall...")

elif menu == "🛡️ Safety & Escrow":
    st.session_state.zimi_mood = ZIMI_THINKING
    st.markdown("<h1 style='text-align:center;'>🛡️ Zimi's Safety Vault</h1>", unsafe_allow_html=True)
    st.info("💡 **Zimi's Tip:** 'Your money stays in our vault until you say the item is clean!'")
    st.markdown("""
    ### 🛡️ Why use ConfirmAm Escrow?
    * **Anti-Scam:** We hold the money, not the seller.
    * **Quality Check:** Verify before you release funds.
    * **No Stress:** If it's "wash," you get your money back.
    """)

elif menu == "📥 Merchant Portal":
    st.session_state.zimi_mood = ZIMI_WAVING
    st.markdown("<h1 style='text-align:center;'>Merchant Portal</h1>", unsafe_allow_html=True)
    with st.form("merchant_reg"):
        st.subheader("Business Registration")
        b_name = st.text_input("Business Name")
        phone = st.text_input("WhatsApp Number")
        submit = st.form_submit_button("Submit for Review")
        if submit and b_name:
            st.session_state.zimi_mood = ZIMI_HAPPY
            st.success(f"Oshey! {b_name} application received.")
            st.balloons()

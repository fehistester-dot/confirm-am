import streamlit as st
import pandas as pd

# 1. Setup & Logo
st.set_page_config(page_title="ConfirmAm Marketplace", page_icon="🛡️", layout="wide")

# 2. CONFIGURATION
SHEET_ID = "1-19BcEQqsLvRKoUX3opcah88GT6veC_8arPqryiJBWs"
PRODUCTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Sheet1"
MERCHANTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=merchants"

# --- Business Logic ---
USD_RATE = 1500  # ₦ to $1 exchange rate
COMMISSION_RATE = 0.10  # Your 10% cut
FLUTTERWAVE_LINK = "https://flutterwave.com/pay/ctppxixgdke7"

# 3. Styling
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    .product-card { background: white; padding: 15px; border-radius: 15px; border: 1px solid #eee; text-align: center; margin-bottom: 20px; }
    .price-text { color: #1DA1F2; font-weight: 800; font-size: 1.2em; }
    .verified-badge { color: #1DA1F2; font-size: 0.8em; font-weight: bold; border: 1px solid #1DA1F2; padding: 2px 5px; border-radius: 5px; }
    .trust-bar { background-color: #e1f5fe; padding: 10px; border-radius: 10px; text-align: center; margin-bottom: 20px; border: 1px dashed #01579b; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (Currency & Nav) ---
st.sidebar.image("https://i.postimg.cc/mD3WvH5n/Confirm-Am-Logo-Tick.png", use_container_width=True)
st.sidebar.title("ConfirmAm")
currency = st.sidebar.radio("💰 Select Currency", ["Naira (₦)", "Dollar ($)"])
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigate", ["🛍️ Shopping Mall", "🛡️ Safety & Escrow", "🏢 Merchant Directory", "📥 Apply to Sell"])

# --- 🛍️ SHOPPING MALL (With Search & Commission) ---
if menu == "🛍️ Shopping Mall":
    st.markdown('<h1 style="text-align:center;">ConfirmAm Mall</h1>', unsafe_allow_html=True)
    st.markdown('<div class="trust-bar">🛡️ <b>Escrow Protected:</b> Money held safely until delivery.</div>', unsafe_allow_html=True)
    
    # SEARCH BAR
    search_query = st.text_input("🔍 Search products...", "").lower()

    try:
        data = pd.read_csv(PRODUCTS_URL)
        data.columns = [c.strip().lower() for c in data.columns]
        
        # Filter Logic
        items = data[(data['status'].str.lower() == 'active') & 
                     (data['name'].str.lower().str.contains(search_query))]

        if items.empty:
            st.info("No items found. Try a different search!")
        else:
            cols = st.columns(2)
            for i, row in items.iterrows():
                with cols[i % 2]:
                    # Currency Logic
                    raw_p = row.get('price', 0)
                    price_display = f"₦{raw_p:,}" if currency == "Naira (₦)" else f"${(raw_p/USD_RATE):,.2f}"
                    
                    st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
                    st.image(row.get('image_url'), use_container_width=True)
                    
                    # Verified Check
                    is_v = str(row.get('verified')).upper() == "TRUE"
                    badge = '<span class="verified-badge">☑️ VERIFIED</span>' if is_v else ""
                    
                    st.markdown(f"<h5>{row.get('name')} {badge}</h5>", unsafe_allow_html=True)
                    st.markdown(f"<p class='price-text'>{price_display}</p>", unsafe_allow_html=True)
                    
                    # Secret Commission (Admin View)
                    with st.expander("Admin: Profit Info"):
                        st.write(f"Your 10% Commission: ₦{(raw_p * COMMISSION_RATE):,}")
                    
                    st.link_button("Buy with Escrow", FLUTTERWAVE_LINK, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
    except:
        st.error("Connecting to Warehouse...")

# --- 🛡️ SAFETY & ESCROW ---
elif menu == "🛡️ Safety & Escrow":
    st.header("How ConfirmAm Protects You")
    st.image("https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=800", use_container_width=True)
    st.write("### Our 4-Step Protection Plan:")
    st.write("1. **You Pay:** Funds are held securely by us.\n2. **Vendor Ships:** We authorize the seller to send the item.\n3. **Real-time Logistics:** Shipping calculated via WhatsApp for fair rates.\n4. **Release:** Vendor is paid ONLY after you confirm delivery.")

# --- 🏢 MERCHANT DIRECTORY ---
elif menu == "🏢 Merchant Directory":
    st.header("Our Verified Partners")
    try:
        m_data = pd.read_csv(MERCHANTS_URL)
        m_data.columns = [c.strip().lower() for c in m_data.columns]
        for _, m in m_data.iterrows():
            st.markdown(f"""
            <div style="background:white; padding:15px; border-radius:10px; border:1px solid #eee; margin-bottom:10px;">
                <h4>{m.get('name')} {'☑️' if str(m.get('verified')).upper() == 'TRUE' else ''}</h4>
                <p style="color:#666;">{m.get('category')} | {m.get('socials')}</p>
            </div>
            """, unsafe_allow_html=True)
    except:
        st.warning("No merchants listed yet.")

# --- 📥 APPLY TO SELL ---
elif menu == "📥 Apply to Sell":
    st.header("Join the Marketplace")
    with st.form("Apply"):
        name = st.text_input("Business Name")
        cat = st.selectbox("Category", ["Fashion", "Tech", "Beauty", "Other"])
        if st.form_submit_button("Submit Application"):
            wa_url = f"https://wa.me/2347046481507?text=Merchant%20Application:%20{name}"
            st.link_button("Complete on WhatsApp", wa_url)

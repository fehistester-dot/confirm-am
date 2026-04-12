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
VENDOR_FEE = 0.05  # 5% taken from Vendor payout
BUYER_MARKUP = 0.05 # 5% added to the Buyer price
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

# --- SIDEBAR ---
st.sidebar.image("https://i.postimg.cc/mD3WvH5n/Confirm-Am-Logo-Tick.png", use_container_width=True)
st.sidebar.title("ConfirmAm")
currency = st.sidebar.radio("💰 Select Currency", ["Naira (₦)", "Dollar ($)"])
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigate", ["🛍️ Shopping Mall", "🛡️ Safety & Escrow", "🏢 Merchant Directory", "📥 Apply to Sell"])

# --- 🛍️ SHOPPING MALL ---
if menu == "🛍️ Shopping Mall":
    st.markdown('<h1 style="text-align:center;">ConfirmAm Mall</h1>', unsafe_allow_html=True)
    st.markdown('<div class="trust-bar">🛡️ <b>Escrow Protected:</b> Money held safely until delivery.</div>', unsafe_allow_html=True)
    
    search_query = st.text_input("🔍 Search products...", "").lower()

    try:
        data = pd.read_csv(PRODUCTS_URL)
        data.columns = [c.strip().lower() for c in data.columns]
        
        items = data[(data['status'].str.lower() == 'active') & 
                     (data['name'].str.lower().str.contains(search_query))]

        if items.empty:
            st.info("No items found. Try a different search!")
        else:
            cols = st.columns(2)
            for i, row in items.iterrows():
                with cols[i % 2]:
                    # --- PRICING LOGIC ---
                    base_p = row.get('price', 0)
                    buyer_p = base_p * (1 + BUYER_MARKUP)
                    vendor_p = base_p * (1 - VENDOR_FEE)
                    total_comm = buyer_p - vendor_p
                    
                    price_display = f"₦{buyer_p:,.0f}" if currency == "Naira (₦)" else f"${(buyer_p/USD_RATE):,.2f}"
                    
                    st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
                    st.image(row.get('image_url'), use_container_width=True)
                    
                    is_v = str(row.get('verified')).upper() == "TRUE"
                    badge = '<span class="verified-badge">☑️ VERIFIED</span>' if is_v else ""
                    
                    st.markdown(f"<h5>{row.get('name')} {badge}</h5>", unsafe_allow_html=True)
                    st.markdown(f"<p class='price-text'>{price_display}</p>", unsafe_allow_html=True)
                    
                    with st.expander("💼 Admin: Commission Breakdown"):
                        st.info("Marketplace Owner View")
                        st.write(f"**Buyer Pays:** ₦{buyer_p:,.0f}")
                        st.write(f"**Vendor Receives:** ₦{vendor_p:,.0f}")
                        st.success(f"**Total Profit:** ₦{total_comm:,.0f}")
                    
                    st.link_button("Buy with Escrow", FLUTTERWAVE_LINK, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
    except:
        st.error("Connecting to Warehouse...")

# --- 🛡️ SAFETY & ESCROW ---
elif menu == "🛡️ Safety & Escrow":
    st.header("How ConfirmAm Protects You")
    st.image("https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=800", use_container_width=True)
    st.write("### Our 4-Step Protection Plan:")
    st.write("1. **You Pay:** Funds are held securely.\n2. **Vendor Ships:** We authorize delivery.\n3. **Real-time Logistics:** Shipping handled via WhatsApp.\n4. **Release:** Vendor is paid only after delivery is confirmed.")

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
    
    with st.expander("✨ Commission & Vendor Protection"):
        st.info("Transparency for our Vendors")
        st.write("""
        To ensure platform security and escrow services, ConfirmAm operates on a small commission structure:
        - **Automatic Markup:** We add 5% to your listing price for the buyer to cover transaction fees.
        - **Platform Fee:** We deduct 5% from the final sale to cover escrow management.
        - **Security:** This ensures you are never scammed and your money is guaranteed once the buyer receives the item.
        """)

    with st.form("Merchant Form"):
        biz_name = st.text_input("Business Name")
        biz_cat = st.selectbox("Category", ["Fashion", "Tech", "Beauty", "Home", "Other"])
        email = st.text_input("Email Address")
        socials = st.text_input("Social Media Handle (IG/TikTok)")
        wa_num = st.text_input("WhatsApp Number")
        location = st.text_input("Business Location (City/State)")
        
        submitted = st.form_submit_button("Submit Application")
        
        if submitted:
            if biz_name and wa_num:
                msg = (f"New Merchant Application:%0A"
                       f"- Business: {biz_name}%0A"
                       f"- Category: {biz_cat}%0A"
                       f"- Email: {email}%0A"
                       f"- Socials: {socials}%0A"
                       f"- Location: {location}%0A"
                       f"- WhatsApp: {wa_num}")
                wa_url = f"https://wa.me/2347046481507?text={msg}"
                st.success("Application ready! Click below to send.")
                st.link_button("Complete on WhatsApp", wa_url, type="primary")
            else:
                st.error("Please fill in the Business Name and WhatsApp Number.")

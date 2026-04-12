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
    .featured-label { background: #FFD700; color: black; padding: 2px 10px; border-radius: 10px; font-size: 0.7em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.image("https://i.postimg.cc/mD3WvH5n/Confirm-Am-Logo-Tick.png", use_container_width=True)
st.sidebar.markdown("<h2 style='text-align:center;'>ConfirmAm</h2>", unsafe_allow_html=True)

# OPTION A: Currency Switcher
st.sidebar.markdown("---")
st.sidebar.subheader("🌍 International Pricing")
currency = st.sidebar.selectbox("Select Currency", ["NGN (₦)", "USD ($)"])
exchange_rate = 1600  # You can update this rate as it changes

st.sidebar.markdown("---")
st.sidebar.subheader("🌟 Happy Customers")
st.sidebar.info("'I was scared to pay online, but ConfirmAm held my money until I got my dress. 100% safe!' - *Adesua, Lagos*")

st.sidebar.markdown("---")
st.sidebar.subheader("📦 Customer Service")
st.sidebar.link_button("Track My Order", "https://wa.me/2347046481507?text=Hello%20ConfirmAm,%20I%20just%20paid%20and%20need%20to%20send%20my%20address", use_container_width=True, type="primary")

menu = st.sidebar.radio("Navigation", ["🛍️ Shopping Mall", "🛡️ Safety & Escrow", "📥 Merchant Portal"])

# --- SHOPPING MALL ---
if menu == "🛍️ Shopping Mall":
    st.markdown('<div class="hero-box"><h1>ConfirmAm Mall</h1><p>Verified Items • Secure Escrow • Fast Delivery</p></div>', unsafe_allow_html=True)
    st.markdown("""<div class="trust-bar"><p style="margin:0; color: #01579b; font-size: 0.85em;">🛡️ <b>Escrow Protected:</b> Money held safely until delivery. <br>🚚 <b>Real-time Shipping:</b> Best rates calculated via WhatsApp after payment.</p></div>""", unsafe_allow_html=True)
    
    try:
        data = pd.read_csv(SHEET_URL)
        data.columns = [c.strip().lower() for c in data.columns]
        
        search_query = st.text_input("🔍 Search for products or categories...", "")
        
        if 'status' in data.columns:
            data = data[data['status'].str.lower() == 'active']

        # Apply Search Filter
        if search_query:
            data = data[data['name'].str.contains(search_query, case=False, na=False) | 
                        data.get('category', '').str.contains(search_query, case=False, na=False)]

        # OPTION B: Featured Section
        if 'featured' in data.columns and not search_query:
            featured_items = data[data['featured'].str.upper() == 'YES']
            if not featured_items.empty:
                st.subheader("🌟 Featured Arrivals")
                f_cols = st.columns(len(featured_items))
                for idx, (f_idx, f_row) in enumerate(featured_items.iterrows()):
                    with f_cols[idx]:
                        st.image(f_row.get('image_url'), use_container_width=True)
                        st.markdown(f"**{f_row.get('name')}**")

        st.markdown("---")
        st.subheader("🛍️ All Products")

        # Display Products
        cols = st.columns(2)
        for i, row in data.iterrows():
            with cols[i % 2]:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                st.image(row.get('image_url', 'https://via.placeholder.com/300'), use_container_width=True)
                
                # Currency Conversion Math
                naira_price = row.get('price', 0)
                if currency == "USD ($)":
                    display_price = f"${(naira_price / exchange_rate):,.2f}"
                else:
                    display_price = f"₦{naira_price:,}"
                
                is_v = str(row.get('verified', '')).strip().upper() == "TRUE"
                badge = '<span class="verified-badge">☑️ VERIFIED</span>' if is_v else ""
                
                st.markdown(f"""
                    <p style="font-size:0.75em; color:#666; margin-bottom:5px;">{row.get('seller', 'ConfirmAm')} {badge}</p>
                    <b style="font-size:1.1em; display:block; height:40px;">{row.get('name', 'Item')}</b>
                    <p class="price-text">{display_price}</p>
                    <p class="delivery-tag">🚚 {row.get('delivery', 'Standard Shipping')}</p>
                """, unsafe_allow_html=True)
                
                # Payment Link
                st.link_button("Buy with Escrow", FLUTTERWAVE_LINK, use_container_width=True)
                
                # OPTION C: Invoice/Receipt Generator
                if st.button(f"Generate Receipt for {row.get('name')}", key=f"rec_{i}"):
                    st.toast("Generating Receipt...")
                    st.code(f"CONFIRMAM RECEIPT\nITEM: {row.get('name')}\nPRICE: {display_price}\nSELLER: {row.get('seller')}\nSTATUS: PENDING ESCROW", language="markdown")
                    st.info("👆 Screenshot this receipt and send to WhatsApp after payment!")
                
                st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error("Connecting to global database...")

# --- SAFETY & ESCROW ---
elif menu == "🛡️ Safety & Escrow":
    st.markdown("<h1 style='text-align:center;'>Your Protection is Our Priority</h1>", unsafe_allow_html=True)
    st.markdown("""### 🛡️ How ConfirmAm Escrow Works:\n1. **PAY:** You pay via Flutterwave.\n2. **HOLD:** ConfirmAm holds the funds safely.\n3. **SHIP:** Vendor sends the item.\n4. **RELEASE:** You confirm receipt, then we pay the vendor.""")
    st.image("https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=800", use_container_width=True)

# --- MERCHANT PORTAL ---
elif menu == "📥 Merchant Portal":
    st.header("Become a Verified Vendor")
    with st.form("Merchant Form"):
        biz_name = st.text_input("Business Name")
        biz_type = st.selectbox("Category", ["Fashion", "Electronics", "Beauty", "Other"])
        ig_handle = st.text_input("Instagram/TikTok Handle")
        submitted = st.form_submit_button("Submit Application")
        if submitted:
            st.success("Application received!")

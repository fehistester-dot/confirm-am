import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="ConfirmAm Marketplace", 
    page_icon="🛡️",
    layout="wide"
)

# 2. THE DATABASE LINKS
SHEET_ID = "1-19BcEQqsLvRKoUX3opcah88GT6veC_8arPqryiJBWs"
PRODUCTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Sheet1"
MERCHANTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=merchants"
FLUTTERWAVE_LINK = "https://flutterwave.com/pay/ctppxixgdke7"

# --- ZIMI IMAGE LINKS ---
ZIMI_SIDEBAR = "https://i.postimg.cc/9QdS9nRv/Gemini-Generated-Image-5wc5485wc5485wc5-removebg-preview.png"
ZIMI_MALL = "https://i.postimg.cc/ZKyXbRJ1/Gemini-Generated-Image-5wc5485wc5485wc5-2-removebg-preview.png"
ZIMI_MERCHANT = "https://i.postimg.cc/7h5dTP0K/Gemini-Generated-Image-5wc5485wc5485wc5-1-removebg-preview.png"

# 3. Enhanced Design & Styling
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    .product-card {
        background-color: white; padding: 15px; border-radius: 15px;
        border: 1px solid #eee; margin-bottom: 20px; text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .merchant-row {
        background-color: white; padding: 15px; border-radius: 12px;
        border-left: 5px solid #1DA1F2; margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .category-header {
        background: #1DA1F2; color: white; padding: 8px 15px;
        border-radius: 8px; margin-top: 20px; font-size: 1.1em; font-weight: bold;
    }
    .price-text { color: #1DA1F2; font-weight: 800; font-size: 1.2em; margin: 5px 0; }
    .commission-text { color: #2e7d32; font-size: 0.85em; font-weight: 600; margin-bottom: 10px; }
    .verified-badge { color: #1DA1F2; font-size: 0.8em; font-weight: bold; border: 1px solid #1DA1F2; padding: 2px 5px; border-radius: 5px; }
    .hero-box { background: #1DA1F2; color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 25px; }
    .trust-bar { background-color: #e1f5fe; padding: 10px; border-radius: 10px; text-align: center; margin-bottom: 20px; border: 1px dashed #01579b; }
    .stSidebar [data-testid="stImage"] img { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.image(ZIMI_SIDEBAR, use_container_width=True)
st.sidebar.markdown("<h2 style='text-align:center;'>ConfirmAm</h2>", unsafe_allow_html=True)

# INTERNATIONAL CURRENCY TOGGLE
currency = st.sidebar.radio("Select Currency", ["NGN (₦)", "USD ($)"])
rate = 1500 # Example exchange rate, adjust as needed

st.sidebar.markdown("---")
st.sidebar.subheader("📦 Order Support")
st.sidebar.link_button(
    "Track My Order", 
    "https://wa.me/2347046481507?text=Hello%20ConfirmAm,%20I%20just%20paid%20and%20need%20to%20send%20my%20address", 
    use_container_width=True,
    type="primary"
)

st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigate", ["🛍️ Shopping Mall", "🛡️ Safety & Escrow", "🏢 Merchant Catalog", "📥 Apply to Sell"])

# --- 1. SHOPPING MALL ---
if menu == "🛍️ Shopping Mall":
    st.markdown('<div class="hero-box"><h1>ConfirmAm Mall</h1><p>Verified Items • Secure Escrow • Fast Delivery</p></div>', unsafe_allow_html=True)
    
    # SEARCH BAR
    search_query = st.text_input("🔍 Search products or sellers...", placeholder="What are you looking for?")

    col_a, col_b = st.columns([1, 4])
    with col_a:
        st.image(ZIMI_MALL, width=100)
    with col_b:
        st.markdown("""
            <div style="background-color: #e1f5fe; padding: 15px; border-radius: 10px; border-left: 5px solid #01579b;">
                <p style="margin:0; color: #01579b;">
                    👋 <b>Hello!</b> I'm Zimi. Note: A <b>5% escrow commission</b> is added to ensure your transaction is 100% safe.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="trust-bar"><p style="margin:0; color: #01579b; font-size: 0.85em;">🛡️ <b>Escrow Protected:</b> Money held safely until delivery. <br>🚚 <b>Shipping:</b> Rates calculated via WhatsApp after payment.</p></div>', unsafe_allow_html=True)
    
    try:
        data = pd.read_csv(PRODUCTS_URL)
        data.columns = [c.strip().lower() for c in data.columns]
        if 'status' in data.columns:
            data = data[data['status'].str.lower() == 'active']
        
        # Apply Search Filter
        if search_query:
            data = data[data['name'].str.contains(search_query, case=False) | data['seller'].str.contains(search_query, case=False)]

        if data.empty:
            st.info("🏪 No items found matching your search.")
        else:
            cols = st.columns(2)
            for i, row in data.iterrows():
                with cols[i % 2]:
                    # COMMISSION CALCULATION (5%)
                    base_price = row.get('price', 0)
                    total_with_commission = base_price * 1.05
                    
                    # Currency conversion logic
                    if currency == "USD ($)":
                        display_price = f"${(total_with_commission / rate):,.2f}"
                    else:
                        display_price = f"₦{total_with_commission:,.0f}"

                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    st.image(row.get('image_url', 'https://via.placeholder.com/300'), use_container_width=True)
                    is_v = str(row.get('verified', '')).strip().upper() == "TRUE"
                    badge = '<span class="verified-badge">☑️ VERIFIED</span>' if is_v else ""
                    
                    st.markdown(f"""
                        <p style="font-size:0.75em; color:#666; margin-bottom:5px;">{row.get('seller', 'ConfirmAm')} {badge}</p>
                        <b style="font-size:1.1em; display:block; height:40px;">{row.get('name', 'Item')}</b>
                        <p class="price-text">{display_price}</p>
                        <p class="commission-text">+ 5% Security Fee Included</p>
                    """, unsafe_allow_html=True)
                    st.link_button("Secure Checkout", FLUTTERWAVE_LINK, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error("Connecting to Warehouse... Please refresh.")

# --- 2. SAFETY & ESCROW ---
elif menu == "🛡️ Safety & Escrow":
    st.markdown("<h1 style='text-align:center;'>How Our 5% Fee Protects You</h1>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=800", use_container_width=True)
    
    st.info("ConfirmAm charges a flat 5% commission on all transactions. This fee covers payment processing and our guarantee that your money is safe if the seller fails to deliver.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🛡️ For Buyers")
        st.write("Your 5% ensures we hold the funds until you inspect the item. If it's a scam, you get 100% back.")
    with col2:
        st.subheader("🤝 For Sellers")
        st.write("We verify the buyer has paid before you ship. No more 'fake alert' stories.")
    with col3:
        st.subheader("📞 24/7 Support")
        st.write("Zimi's agents are available to resolve any delivery disputes immediately.")

# --- 3. MERCHANT CATALOG ---
elif menu == "🏢 Merchant Catalog":
    col_m1, col_m2 = st.columns([1, 4])
    with col_m1:
        st.image(ZIMI_MERCHANT, width=120)
    with col_m2:
        st.markdown("<h1>Verified Merchant Catalog</h1>", unsafe_allow_html=True)
    
    try:
        m_data = pd.read_csv(MERCHANTS_URL)
        m_data.columns = [c.strip().lower() for c in m_data.columns]
        categories = m_data['category'].unique()
        for cat in categories:
            st.markdown(f"<div class='category-header'>{cat.upper()} SELLERS</div>", unsafe_allow_html=True)
            cat_vendors = m_data[m_data['category'] == cat]
            for _, m in cat_vendors.iterrows():
                is_mv = str(m.get('verified')).upper() == 'TRUE'
                st.markdown(f"""
                <div class="merchant-row">
                    <span style="font-size:1.1em; font-weight:bold;">{m.get('name', 'Business')}</span> {'☑️' if is_mv else ''}<br>
                    <span style="color:#666; font-size:0.9em;">Socials: {m.get('socials', '')}</span>
                </div>
                """, unsafe_allow_html=True)
    except:
        st.warning("Check your 'merchants' tab in Google Sheets.")

# --- 4. APPLY TO SELL ---
elif menu == "📥 Apply to Sell":
    col_x, col_y = st.columns([1, 3])
    with col_x:
        st.image(ZIMI_MERCHANT, use_container_width=True)
    with col_y:
        st.header("Become a Verified Vendor")
        st.write("Note: ConfirmAm keeps a 5% commission on successful sales for providing the secure platform.")
    
    with st.form("Merchant Form"):
        biz_name = st.text_input("Business Name")
        biz_type = st.selectbox("Category", ["Fashion", "Electronics", "Beauty", "Home", "Other"])
        ig_handle = st.text_input("Social Media Handle (IG/TikTok)")
        contact = st.text_input("WhatsApp Number")
        
        submitted = st.form_submit_button("Submit Application")
        if submitted:
            msg = f"New%20Merchant%20Application:%0AName:%20{biz_name}%0ACategory:%20{biz_type}%0AHandle:%20{ig_handle}%0APhone:%20{contact}"
            wa_url = f"https://wa.me/2347046481507?text={msg}"
            st.success("Zimi is ready to verify you!")
            st.link_button("Open WhatsApp to Finish", wa_url, type="primary")

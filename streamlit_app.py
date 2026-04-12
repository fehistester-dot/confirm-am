import streamlit as st
import pandas as pd

# 1. Page Configuration & Logo
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
    .price-text { color: #1DA1F2; font-weight: 800; font-size: 1.3em; margin: 10px 0; }
    .verified-badge { color: #1DA1F2; font-size: 0.8em; font-weight: bold; border: 1px solid #1DA1F2; padding: 2px 5px; border-radius: 5px; }
    .hero-box { background: #1DA1F2; color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 25px; }
    .trust-bar { background-color: #e1f5fe; padding: 10px; border-radius: 10px; text-align: center; margin-bottom: 20px; border: 1px dashed #01579b; }
    
    .stSidebar [data-testid="stImage"] img { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.image(ZIMI_SIDEBAR, use_container_width=True)
st.sidebar.markdown("<h2 style='text-align:center;'>ConfirmAm</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align:center; color:#666; font-size:0.9em;'>Welcome, I am Zimi! 🛡️<br>Your Escrow Guide.</p>", unsafe_allow_html=True)
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
    
    col_a, col_b = st.columns([1, 4])
    with col_a:
        st.image(ZIMI_MALL, width=100)
    with col_b:
        st.markdown("""
            <div style="background-color: #e1f5fe; padding: 15px; border-radius: 10px; border-left: 5px solid #01579b;">
                <p style="margin:0; color: #01579b;">
                    👋 <b>Hello there!</b> I'm Zimi. I've personally verified these listings. Remember, your money is safe with us until you get your item. Happy Shopping!
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="trust-bar"><p style="margin:0; color: #01579b; font-size: 0.85em;">🛡️ <b>Escrow Protected:</b> Money held safely until delivery. <br>🚚 <b>Real-time Shipping:</b> Rates calculated via WhatsApp after payment.</p></div>', unsafe_allow_html=True)
    
    try:
        data = pd.read_csv(PRODUCTS_URL)
        data.columns = [c.strip().lower() for c in data.columns]
        if 'status' in data.columns:
            data = data[data['status'].str.lower() == 'active']
        
        if data.empty:
            st.info("🏪 Zimi is stocking the shelves. Check back in a moment!")
        else:
            cols = st.columns(2)
            for i, row in data.iterrows():
                with cols[i % 2]:
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    st.image(row.get('image_url', 'https://via.placeholder.com/300'), use_container_width=True)
                    is_v = str(row.get('verified', '')).strip().upper() == "TRUE"
                    badge = '<span class="verified-badge">☑️ VERIFIED</span>' if is_v else ""
                    st.markdown(f"""
                        <p style="font-size:0.75em; color:#666; margin-bottom:5px;">{row.get('seller', 'ConfirmAm')} {badge}</p>
                        <b style="font-size:1.1em; display:block; height:40px;">{row.get('name', 'Item')}</b>
                        <p class="price-text">₦{row.get('price', 0):,}</p>
                    """, unsafe_allow_html=True)
                    st.link_button("Buy with Escrow", FLUTTERWAVE_LINK, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error("Connecting to Warehouse... Please refresh.")

# --- 2. SAFETY & ESCROW ---
elif menu == "🛡️ Safety & Escrow":
    st.markdown("<h1 style='text-align:center;'>Your Protection is Our Priority</h1>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=800", use_container_width=True)
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🛡️ Scam Prevention")
        st.write("ConfirmAm/Zimi acts as your middleman. We verify payment first. The vendor only ships once funds are secured.")
    with col2:
        st.subheader("🚚 Fair Delivery")
        st.write("Rates are calculated via WhatsApp after payment to ensure you get the most accurate prices.")
    with col3:
        st.subheader("🤝 Direct Support")
        st.write("Our WhatsApp agents track your order from the moment you pay until the item is in your hands.")
    st.info("💡 **Zimi keeps your money safe. Sellers are only paid when you confirm you've received your item.**")

# --- 3. MERCHANT CATALOG (Organized Grouping) ---
elif menu == "🏢 Merchant Catalog":
    col_m1, col_m2 = st.columns([1, 4])
    with col_m1:
        st.image(ZIMI_MERCHANT, width=120)
    with col_m2:
        st.markdown("<h1>Verified Merchant Catalog</h1>", unsafe_allow_html=True)
        st.write("Browse our trusted partners by category.")

    try:
        m_data = pd.read_csv(MERCHANTS_URL)
        m_data.columns = [c.strip().lower() for c in m_data.columns]
        
        if m_data.empty:
            st.info("Zimi is currently verifying new merchants. Check back soon!")
        else:
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
        st.warning("Check your 'merchants' tab headers: name, category, socials, contact, verified")

# --- 4. APPLY TO SELL ---
elif menu == "📥 Apply to Sell":
    col_x, col_y = st.columns([1, 3])
    with col_x:
        st.image(ZIMI_MERCHANT, use_container_width=True)
    with col_y:
        st.header("Become a Verified Vendor")
        st.write("Join the most trusted marketplace. Fill this out and Zimi will connect with you via WhatsApp.")
    
    with st.form("Merchant Form"):
        biz_name = st.text_input("Business Name")
        biz_type = st.selectbox("Category", ["Fashion", "Electronics", "Beauty", "Other"])
        ig_handle = st.text_input("Instagram/TikTok Handle")
        contact = st.text_input("WhatsApp Number")
        submitted = st.form_submit_button("Submit Application")
        if submitted:
            msg = f"Merchant Application:%20{biz_name}%0ACategory:%20{biz_type}%0ASocials:%20{ig_handle}%0AContact:%20{contact}"
            wa_url = f"https://wa.me/2347046481507?text={msg}"
            st.success("Zimi is preparing your WhatsApp verification...")
            st.link_button("Complete Application on WhatsApp", wa_url, type="primary")

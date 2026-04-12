import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="ConfirmAm Marketplace", 
    page_icon="🛡️",
    layout="wide"
)

# 2. THE DATABASE LINKS - THE STABLEST VERSION
SHEET_ID = "1VubDpOo8wOWTOeyhgu-9oMlagyTvRZUqDc6wkXIpfTY"

# Using the /export method which is much faster for mobile apps
PRODUCTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
MERCHANTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1626214553"

FLUTTERWAVE_LINK = "https://flutterwave.com/pay/ctppxixgdke7"

# --- ZIMI IMAGE LINKS ---
ZIMI_SIDEBAR = "https://i.postimg.cc/9QdS9nRv/Gemini-Generated-Image-5wc5485wc5485wc5-removebg-preview.png"
ZIMI_MALL = "https://i.postimg.cc/ZKyXbRJ1/Gemini-Generated-Image-5wc5485wc5485wc5-2-removebg-preview.png"
ZIMI_MERCHANT = "https://i.postimg.cc/7h5dTP0K/Gemini-Generated-Image-5wc5485wc5485wc5-1-removebg-preview.png"

# 3. Styling
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    .product-card {
        background-color: white; padding: 12px; border-radius: 15px;
        border: 1px solid #eee; margin-bottom: 20px; text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); transition: 0.3s;
    }
    .product-card:hover { transform: translateY(-5px); box-shadow: 0 8px 15px rgba(0,0,0,0.1); }
    .price-text { color: #1DA1F2; font-weight: 800; font-size: 1.2em; margin: 8px 0; }
    .hero-box { background: linear-gradient(135deg, #1DA1F2 0%, #01579b 100%); color: white; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 25px; }
    .vendor-tag { background: #e1f5fe; color: #01579b; font-size: 0.7em; padding: 2px 8px; border-radius: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.image(ZIMI_SIDEBAR, use_container_width=True)
st.sidebar.markdown("<h2 style='text-align:center;'>ConfirmAm</h2>", unsafe_allow_html=True)

currency = st.sidebar.selectbox("Display Currency", ["🇳🇬 NGN (Naira)", "🇺🇸 USD (Dollar)"])
rate = 1500 
symbol = "₦" if "NGN" in currency else "$"

st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigate", ["🛍️ Shopping Mall", "🏢 Merchant Catalog", "🛡️ How Escrow Works", "📥 Apply to Sell"])

# --- 1. SHOPPING MALL ---
if menu == "🛍️ Shopping Mall":
    st.markdown('<div class="hero-box"><h1>ConfirmAm Mall</h1><p>Premium Selections • Verified Vendors • Secure Payments</p></div>', unsafe_allow_html=True)
    
    # Simple Search
    search_query = st.text_input("🔍 Search products...", "").lower()

    try:
        # Added on_bad_lines='skip' so one bad row doesn't break the whole app
        data = pd.read_csv(PRODUCTS_URL, on_bad_lines='skip')
        data.columns = [c.strip().lower() for c in data.columns]
        
        if search_query:
            data = data[data['name'].str.lower().str.contains(search_query, na=False)]

        if data.empty:
            st.info("The Mall is currently being updated. Check back in a moment!")
        else:
            cols = st.columns(2 if st.sidebar.checkbox("Mobile View", True) else 5)
            for i, (idx, row) in enumerate(data.iterrows()):
                with cols[i % len(cols)]:
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    st.image(row.get('image_url', ''), use_container_width=True)
                    
                    # Safe price conversion
                    try:
                        price = float(row.get('price', 0)) * 1.05
                    except:
                        price = 0
                        
                    display_price = price if symbol == "₦" else (price / rate)
                    
                    st.markdown(f"""
                        <span class="vendor-tag">👤 {row.get('seller', 'Verified')}</span>
                        <b style="font-size:0.9em; display:block; margin-top:10px;">{row.get('name', 'Product')}</b>
                        <p class="price-text">{symbol}{display_price:,.0f}</p>
                    """, unsafe_allow_html=True)
                    st.link_button("Instant Buy", FLUTTERWAVE_LINK, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
    except:
        st.error("Zimi is refreshing the stock. Please click 'Always Allow' if your browser asks for permission.")

# --- 2. MERCHANT CATALOG ---
elif menu == "🏢 Merchant Catalog":
    st.title("Verified Partners")
    try:
        m_data = pd.read_csv(MERCHANTS_URL, on_bad_lines='skip')
        m_data.columns = m_data.columns.str.strip().str.lower()
        
        for _, m in m_data.iterrows():
            with st.container():
                st.markdown(f"✅ **{m.iloc[0]}**")
                st.caption(f"Handle: {m.get('socials', m.get('instagram/tiktok handle', 'Contact Admin'))}")
                st.markdown("---")
    except:
        st.warning("Merchant directory is updating...")

# --- 3. SAFETY ---
elif menu == "🛡️ How Escrow Works":
    st.header("The Zimi Guarantee")
    st.write("1. We hold the money. 2. You get the goods. 3. Vendor gets paid.")

# --- 4. APPLY ---
elif menu == "📥 Apply to Sell":
    st.title("Partner with ConfirmAm")
    with st.form("Apply"):
        name = st.text_input("Business Name")
        email = st.text_input("Email")
        if st.form_submit_button("Submit"):
            st.success("Redirecting...")
            st.link_button("Finish on WhatsApp", f"https://wa.me/2347046481507?text=Apply:{name}")

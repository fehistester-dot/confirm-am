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
        background-color: white; padding: 10px; border-radius: 12px;
        border: 1px solid #eee; margin-bottom: 20px; text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); transition: 0.3s;
    }
    .product-card:hover { transform: translateY(-5px); box-shadow: 0 6px 12px rgba(0,0,0,0.1); }
    .price-text { color: #1DA1F2; font-weight: 800; font-size: 1.1em; margin: 5px 0; }
    .commission-text { color: #28a745; font-size: 0.75em; font-weight: bold; }
    .hero-box { background: #1DA1F2; color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px; }
    .stSidebar [data-testid="stImage"] img { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR & GLOBAL SETTINGS ---
st.sidebar.image(ZIMI_SIDEBAR, use_container_width=True)
st.sidebar.markdown("<h2 style='text-align:center;'>ConfirmAm</h2>", unsafe_allow_html=True)

# Currency Toggle
currency = st.sidebar.radio("Currency / Local Exchange", ["🇳🇬 NGN (Naira)", "🇺🇸 USD (Dollar)"])
rate = 1500 # Current average exchange rate - you can update this manually
symbol = "₦" if "NGN" in currency else "$"

st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigate", ["🛍️ Shopping Mall", "🛡️ Safety & Escrow", "🏢 Merchant Catalog", "📥 Apply to Sell"])

# --- 1. SHOPPING MALL ---
if menu == "🛍️ Shopping Mall":
    st.markdown('<div class="hero-box"><h1>ConfirmAm Mall</h1><p>Verified Items • Secure Escrow • 5% Flat Commission</p></div>', unsafe_allow_html=True)
    
    # Search Bar
    search_query = st.text_input("🔍 Search for products or vendors...", "").lower()

    col_a, col_b = st.columns([1, 5])
    with col_a:
        st.image(ZIMI_MALL, width=80)
    with col_b:
        st.info(f"👋 **Zimi here!** Browse our verified items. Note: A tiny **5% escrow fee** is added to secure your deal.")

    try:
        data = pd.read_csv(PRODUCTS_URL)
        data.columns = [c.strip().lower() for c in data.columns]
        
        # Filter Active & Search
        if 'status' in data.columns:
            data = data[data['status'].str.lower() == 'active']
        
        if search_query:
            data = data[data['name'].str.lower().str.contains(search_query) | 
                        data['seller'].str.lower().str.contains(search_query)]

        if data.empty:
            st.warning("No products found. Try a different search!")
        else:
            # 5 COLUMN GRID
            cols = st.columns(5)
            for i, row in data.iterrows():
                with cols[i % 5]:
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    st.image(row.get('image_url', ''), use_container_width=True)
                    
                    # Math for Commission & Currency
                    raw_price = float(row.get('price', 0))
                    total_price = raw_price * 1.05 # Add 5% commission
                    
                    display_price = total_price if symbol == "₦" else (total_price / rate)
                    
                    st.markdown(f"""
                        <b style="font-size:0.9em; display:block; height:35px; overflow:hidden;">{row.get('name', 'Item')}</b>
                        <p class="price-text">{symbol}{display_price:,.0f}</p>
                        <p class="commission-text">+5% Protection Fee Incl.</p>
                    """, unsafe_allow_html=True)
                    st.link_button("Buy Securely", FLUTTERWAVE_LINK, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error("Warehouse connection lost. Please refresh.")

# --- 2. SAFETY & ESCROW ---
elif menu == "🛡️ Safety & Escrow":
    st.header("The ConfirmAm 5% Guarantee")
    st.markdown("""
    To keep your transactions 100% safe, we charge a small **5% commission** from both parties. 
    This covers:
    * **Verification:** Ensuring the vendor is real.
    * **Escrow:** Holding your funds in a secure vault.
    * **Dispute Resolution:** Zimi steps in if the item isn't what you ordered.
    """)
    st.image("https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=800", use_container_width=True)

# --- 3. MERCHANT CATALOG ---
elif menu == "🏢 Merchant Catalog":
    col_m1, col_m2 = st.columns([1, 4])
    with col_m1: st.image(ZIMI_MERCHANT, width=120)
    with col_m2: st.title("Verified Merchant Directory")

    try:
        m_data = pd.read_csv(MERCHANTS_URL)
        m_data.columns = [c.strip().lower() for c in m_data.columns]
        
        for cat in m_data['category'].unique():
            st.subheader(f"🏷️ {cat.upper()}")
            cat_vendors = m_data[m_data['category'] == cat]
            for _, m in cat_vendors.iterrows():
                st.info(f"**{m.get('name')}** - {m.get('socials')} (Verified ☑️)")
    except:
        st.error("Error loading Merchant list.")

# --- 4. APPLY TO SELL ---
elif menu == "📥 Apply to Sell":
    st.title("Join ConfirmAm as a Vendor")
    st.write("Sell to thousands of verified buyers with Zimi's protection.")
    
    with st.form("Merchant Form"):
        biz_name = st.text_input("Business Name")
        biz_type = st.selectbox("Category", ["Fashion", "Electronics", "Beauty", "Home", "Other"])
        ig_handle = st.text_input("Social Media Handle (IG/TikTok)")
        phone = st.text_input("WhatsApp Number")
        
        st.write("⚠️ *Note: ConfirmAm takes a 5% commission on all successful sales to provide escrow services.*")
        
        if st.form_submit_button("Submit Application"):
            msg = f"New%20Merchant:%20{biz_name}%0ACategory:%20{biz_type}%0ASocials:%20{ig_handle}"
            st.success("Zimi is reviewing your request...")
            st.link_button("Chat with Zimi to Finish", f"https://wa.me/2347046481507?text={msg}")

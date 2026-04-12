import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="ConfirmAm Marketplace", 
    page_icon="🛡️",
    layout="wide"
)

# 2. THE DATABASE LINKS
SHEET_ID = "1VubDpOo8wOWTOeyhgu-9oMlagyTvRZUqDc6wkXIpfTY"
# UPDATED GID for Product Form Responses
PRODUCTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1271207401"
MERCHANTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1626214553"

# Link to your Product Upload Google Form
PRODUCT_FORM_LINK = "https://docs.google.com/forms/d/e/YOUR_FORM_ID_HERE/viewform" 
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
        background-color: white; padding: 12px; border-radius: 15px;
        border: 1px solid #eee; margin-bottom: 20px; text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); transition: 0.3s;
    }
    .product-card:hover { transform: translateY(-5px); box-shadow: 0 8px 15px rgba(0,0,0,0.1); }
    .price-text { color: #1DA1F2; font-weight: 800; font-size: 1.2em; margin: 8px 0; }
    .hero-box { background: linear-gradient(135deg, #1DA1F2 0%, #01579b 100%); color: white; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 25px; }
    .stSidebar [data-testid="stImage"] img { border-radius: 15px; }
    .vendor-tag { background: #e1f5fe; color: #01579b; font-size: 0.7em; padding: 2px 8px; border-radius: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR & GLOBAL SETTINGS ---
st.sidebar.image(ZIMI_SIDEBAR, use_container_width=True)
st.sidebar.markdown("<h2 style='text-align:center;'>ConfirmAm</h2>", unsafe_allow_html=True)

currency = st.sidebar.selectbox("Display Currency", ["🇳🇬 NGN (Naira)", "🇺🇸 USD (Dollar)"])
rate = 1500 
symbol = "₦" if "NGN" in currency else "$"

st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigate", ["🛍️ Shopping Mall", "🏢 Merchant Catalog", "🛡️ How Escrow Works", "📥 Apply to Sell"])

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 ConfirmAm Nigeria. All transactions are Escrow-Protected.")

# --- 1. SHOPPING MALL ---
if menu == "🛍️ Shopping Mall":
    st.markdown('<div class="hero-box"><h1>ConfirmAm Mall</h1><p>Premium Selections • Verified Vendors • Secure Payments</p></div>', unsafe_allow_html=True)
    
    s_col1, s_col2 = st.columns([3, 1])
    with s_col1:
        search_query = st.text_input("🔍 Search for products...", "").lower()
    with s_col2:
        category_filter = st.selectbox("Quick Filter", ["All Items", "Fashion", "Electronics", "Beauty", "Home"])

    try:
        data = pd.read_csv(PRODUCTS_URL)
        data.columns = [c.strip().lower() for c in data.columns]
        
        # Check if 'status' column exists to avoid errors
        if 'status' in data.columns:
            data = data[data['status'].astype(str).str.lower() == 'active']
        
        if not data.empty:
            if search_query:
                # Flexible search across name and seller
                name_match = data['product name'].astype(str).str.lower().str.contains(search_query) if 'product name' in data.columns else data.iloc[:,1].astype(str).str.lower().str.contains(search_query)
                data = data[name_match]
            
            if category_filter != "All Items":
                cat_match = data['category / niche'].astype(str).str.lower() == category_filter.lower() if 'category / niche' in data.columns else data.iloc[:,2].astype(str).str.lower() == category_filter.lower()
                data = data[cat_match]

        if data.empty:
            st.info("The Mall is being restocked! Check back in a few minutes.")
        else:
            cols = st.columns(5)
            for i, row in data.iterrows():
                with cols[i % 5]:
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    img = row.get('product image link', row.get('image_url', ''))
                    st.image(img, use_container_width=True)
                    
                    try:
                        price_val = float(row.get('price (naira)', row.get('price', 0)))
                    except:
                        price_val = 0
                        
                    final_amt = price_val * 1.05 
                    display_price = final_amt if symbol == "₦" else (final_amt / rate)
                    
                    name = row.get('product name', 'Premium Item')
                    seller = row.get('seller / business name', 'Verified Seller')
                    
                    st.markdown(f"""
                        <span class="vendor-tag">👤 {seller}</span>
                        <b style="font-size:0.9em; display:block; margin-top:10px; height:40px; overflow:hidden;">{name}</b>
                        <p class="price-text">{symbol}{display_price:,.0f}</p>
                    """, unsafe_allow_html=True)
                    st.link_button("Instant Buy", FLUTTERWAVE_LINK, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
    except Exception:
        st.warning("Zimi is updating the shelves. Please refresh in a moment!")

# --- 2. MERCHANT CATALOG ---
elif menu == "🏢 Merchant Catalog":
    col_m1, col_m2 = st.columns([1, 4])
    with col_m1: st.image(ZIMI_MERCHANT, width=120)
    with col_m2: st.title("Verified Partners")

    try:
        m_data = pd.read_csv(MERCHANTS_URL)
        m_data.columns = m_data.columns.str.strip().str.lower()
        
        if m_data.empty:
            st.info("Zimi is currently vetting new merchants. Check back soon!")
        else:
            cat_col = 'category' if 'category' in m_data.columns else 'niche'
            if cat_col in m_data.columns:
                for cat in m_data[cat_col].unique():
                    if pd.isna(cat): continue
                    with st.expander(f"📁 {str(cat).upper()} VENDORS", expanded=True):
                        cat_vendors = m_data[m_data[cat_col] == cat]
                        for _, m in cat_vendors.iterrows():
                            v_name = m.get('name', m.get('business name', 'Unknown Business'))
                            v_social = m.get('socials', m.get('instagram/tiktok handle', 'No social link'))
                            st.markdown(f"✅ **{v_name}** | Socials: `{v_social}`")
            else:
                st.write("### All Verified Vendors")
                for _, m in m_data.iterrows():
                    st.markdown(f"✅ **{m.iloc[0]}**")
    except Exception:
        st.error("Could not load merchant list. Refreshing...")

# --- 3. SAFETY & ESCROW ---
elif menu == "🛡️ How Escrow Works":
    st.image(ZIMI_SIDEBAR, width=150)
    st.header("The Zimi Guarantee")
    st.markdown("""
    ### Why Shop with ConfirmAm?
    1. **Secured Funds:** We hold your payment in a neutral vault.
    2. **Verified Quality:** Vendors only get paid once the item is delivered.
    3. **No Scams:** We vet every merchant so you don't have to.
    """)
    st.link_button("Contact Support", "https://wa.me/2347046481507")

# --- 4. APPLY TO SELL ---
elif menu == "📥 Apply to Sell":
    st.title("Partner with ConfirmAm")
    st.write("Join Nigeria's most trusted escrow marketplace.")
    
    # Check if they just submitted
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    if not st.session_state.submitted:
        with st.form("Merchant Form"):
            b_name = st.text_input("Business Name")
            b_cat = st.selectbox("Niche", ["Fashion", "Electronics", "Beauty", "Services", "Other"])
            b_email = st.text_input("Email Address")
            b_social = st.text_input("Instagram/TikTok Handle")
            b_phone = st.text_input("WhatsApp Number")
            
            if st.form_submit_button("Submit Application"):
                msg = f"App:%20{b_name}%0ACat:%20{b_cat}%0AEmail:%20{b_email}%0ASocial:%20{b_social}"
                st.session_state.submitted = True
                st.rerun()
    else:
        st.success("✅ Application Sent! Zimi is reviewing your details.")
        st.info("Step 2: Upload your products to the Mall using the button below.")
        col1, col2 = st.columns(2)
        with col1:
            st.link_button("🚀 UPLOAD PRODUCTS", PRODUCT_FORM_LINK, use_container_width=True)
        with col2:
            st.link_button("💬 CHAT WITH ADMIN", "https://wa.me/2347046481507", use_container_width=True)
        
        if st.button("Submit another application"):
            st.session_state.submitted = False
            st.rerun()

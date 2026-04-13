import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. Page Configuration
st.set_page_config(
    page_title="ConfirmAm Marketplace", 
    page_icon="🛡️",
    layout="wide"
)

# 2. THE DATABASE LINKS & CONFIG
PRODUCT_SHEET_ID = "1-19BcEQqsLvRKoUX3opcah88GT6veC_8arPqryiJBWs"
MERCHANT_SHEET_ID = "1WniAk7CLPVev8qGGwFlah6SwnTeDUT1qJhHM3XslSXU"
WHATSAPP_NUMBER = "2349136533490" 

PRODUCTS_URL = f"https://docs.google.com/spreadsheets/d/{PRODUCT_SHEET_ID}/export?format=csv&gid=0"
MERCHANTS_URL = f"https://docs.google.com/spreadsheets/d/{MERCHANT_SHEET_ID}/export?format=csv&gid=0"
FLUTTERWAVE_LINK = "https://flutterwave.com/pay/ctppxixgdke7"

ZIMI_SIDEBAR = "https://i.postimg.cc/9QdS9nRv/Gemini-Generated-Image-5wc5485wc5485wc5-removebg-preview.png"

def load_sheet_data(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        df = pd.read_csv(StringIO(response.text), on_bad_lines='skip')
        # We clean the column names strictly
        df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
        return df.dropna(how='all')
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return pd.DataFrame()

# 3. Styling
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    .product-card {
        background-color: white; padding: 20px; border-radius: 15px;
        border: 1px solid #eee; margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .price-text { color: #1DA1F2; font-weight: 800; font-size: 1.8em; margin: 5px 0; }
    .vendor-tag { background: #e1f5fe; color: #01579b; font-size: 0.8em; padding: 4px 10px; border-radius: 20px; font-weight: bold; }
    .character-header {
        display: flex; align-items: center; gap: 20px; background: white; padding: 15px; border-radius: 15px; border: 1px solid #eee; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.image(ZIMI_SIDEBAR, use_container_width=True)
currency = st.sidebar.selectbox("Display Currency", ["🇳🇬 NGN (Naira)", "🇺🇸 USD (Dollar)"])
rate = 1500 
symbol = "₦" if "NGN" in currency else "$"

st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigate", ["🛍️ Shopping Mall", "🏢 Merchant Catalog", "🛡️ How Escrow Works", "📥 Apply to Sell", "📢 Advertise Product", "📞 Contact Support"])

# --- 1. SHOPPING MALL ---
if menu == "🛍️ Shopping Mall":
    st.markdown(f"""
        <div class="character-header">
            <img src="{ZIMI_SIDEBAR}" width="100">
            <div>
                <h1 style="margin:0; color:#1DA1F2;">ConfirmAm Mall</h1>
                <p style="margin:0; color:#666;"><b>Captain Zimi:</b> "Pick your size and color below. I'll handle the rest!"</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    data = load_sheet_data(PRODUCTS_URL)
    
    if not data.empty:
        # Search Filter
        search = st.text_input("🔍 Search products...", "").lower()
        if search:
            data = data[data['name'].str.lower().str.contains(search, na=False)]

        for idx, row in data.iterrows():
            with st.container():
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                col1, col2 = st.columns([1, 1.5])
                
                with col1:
                    img = row.get('image_url', row.get('image', ''))
                    st.image(img, use_container_width=True)

                with col2:
                    st.markdown(f"## {row.get('name', 'Product')}")
                    st.markdown(f'<span class="vendor-tag">👤 Vendor: {row.get("seller", "Verified")}</span>', unsafe_allow_html=True)
                    
                    st.write("---")
                    
                    # --- THE SELECTION SECTION ---
                    s_col1, s_col2, s_col3 = st.columns(3)
                    
                    # 🎨 Colors
                    colors = str(row.get('available_colors', 'Default')).split(',')
                    sel_color = s_col1.selectbox("Select Color", [c.strip() for c in colors], key=f"c{idx}")
                    
                    # 📏 Sizes
                    sizes = str(row.get('available_sizes', 'Standard')).split(',')
                    sel_size = s_col2.selectbox("Select Size", [s.strip() for s in sizes], key=f"s{idx}")
                    
                    # 🔢 Quantity
                    sel_qty = s_col3.number_input("Quantity", 1, 10, 1, key=f"q{idx}")

                    # Price Calculation
                    raw_price = float(row.get('price', 0)) * 1.05
                    total = (raw_price if symbol == "₦" else (raw_price / rate)) * sel_qty
                    st.markdown(f"<div class='price-text'>{symbol}{total:,.0f}</div>", unsafe_allow_html=True)

                    # --- ACTION BUTTONS ---
                    b_col1, b_col2 = st.columns(2)
                    
                    with b_col1:
                        st.link_button("💳 Instant Buy", FLUTTERWAVE_LINK, use_container_width=True)
                    
                    with b_col2:
                        msg = f"Hello, I want to order:\n📦 *{row.get('name')}*\n🎨 Color: {sel_color}\n📏 Size: {sel_size}\n🔢 Qty: {sel_qty}\n💰 Total: {symbol}{total:,.0f}"
                        wa_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={requests.utils.quote(msg)}"
                        st.link_button("💬 Order on WhatsApp", wa_url, use_container_width=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No products found. Please check your Google Sheet headers.")

# --- THE REST OF THE PAGES (UNCHANGED TO PRESERVE SETTINGS) ---
elif menu == "🏢 Merchant Catalog":
    st.title("Verified Merchants")
    m_data = load_sheet_data(MERCHANTS_URL)
    if not m_data.empty:
        for _, row in m_data.iterrows():
            with st.expander(f"✅ {str(row.iloc[0]).upper()}"):
                st.write(f"**Niche:** {row.get('niche', 'General')}")
                st.write(f"**Socials:** {row.get('socials', 'Verified')}")
    else: st.info("Loading Merchants...")

elif menu == "🛡️ How Escrow Works":
    st.header("The Zimi Guarantee")
    st.markdown("""
    1. **Secure Payment:** Zimi holds the money.
    2. **Verification:** You get your item and check it.
    3. **Release:** Zimi pays the seller only after you are happy!
    """)

elif menu == "📥 Apply to Sell":
    with st.form("Apply"):
        st.text_input("Business Name")
        if st.form_submit_button("Submit"): st.success("Zimi will contact you!")

elif menu == "📢 Advertise Product":
    with st.form("Ad"):
        st.text_input("Product Name")
        if st.form_submit_button("Submit"): st.info("Reviewing your ad...")

elif menu == "📞 Contact Support":
    st.link_button("Chat with Support", f"https://wa.me/{WHATSAPP_NUMBER}")

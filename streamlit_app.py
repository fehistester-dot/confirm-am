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
        # Clean column names to prevent the "nan" issues seen in your screenshot
        df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
        return df.dropna(how='all')
    except:
        return pd.DataFrame()

# 3. Styling
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    .product-card {
        background-color: white; padding: 20px; border-radius: 15px;
        border: 1px solid #eee; margin-bottom: 25px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .price-text { color: #1DA1F2; font-weight: 800; font-size: 1.5em; margin: 8px 0; }
    .vendor-tag { background: #e1f5fe; color: #01579b; font-size: 0.8em; padding: 4px 10px; border-radius: 20px; font-weight: bold; }
    .sale-badge { background: #ff4b4b; color: white; padding: 4px 12px; border-radius: 10px; font-weight: bold; font-size: 0.8em; margin-bottom: 5px; display: inline-block; }
    .stock-badge { color: #ff4b4b; font-weight: bold; border: 1px solid #ff4b4b; padding: 2px 8px; border-radius: 5px; font-size: 0.8em; display: inline-block; }
    .character-header { display: flex; align-items: center; gap: 20px; background: white; padding: 15px; border-radius: 15px; border: 1px solid #eee; margin-bottom: 20px; }
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
    st.markdown(f'<div class="character-header"><img src="{ZIMI_SIDEBAR}" width="100"><div><h1 style="margin:0; color:#1DA1F2;">ConfirmAm Mall</h1><p style="margin:0; color:#666;"><b>Captain Zimi:</b> "Safe shopping only!"</p></div></div>', unsafe_allow_html=True)
    
    search_query = st.text_input("🔍 Search products...", "").lower()
    data = load_sheet_data(PRODUCTS_URL)

    if not data.empty:
        if search_query:
            data = data[data['name'].str.lower().str.contains(search_query, na=False)]

        for idx, row in data.iterrows():
            # Handle possible "nan" values from the sheet
            p_name = str(row.get('name', 'Product'))
            p_seller = str(row.get('seller', 'Verified Vendor'))
            
            is_out = str(row.get('status', '')).lower() == "out of stock"
            is_sale = str(row.get('on_sale', '')).lower() == "yes"

            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            col1, col2 = st.columns([1, 2])
            
            with col1:
                img_url = row.get('image_url', row.get('image', ''))
                if pd.isna(img_url) or img_url == "":
                    st.warning("No Image")
                else:
                    st.image(img_url, use_container_width=True)

            with col2:
                if is_sale: st.markdown('<span class="sale-badge">🔥 SALE</span>', unsafe_allow_html=True)
                if is_out: st.markdown('<span class="stock-badge">🚫 SOLD OUT</span>', unsafe_allow_html=True)
                
                st.markdown(f"### {p_name}")
                st.markdown(f'<span class="vendor-tag">👤 {p_seller}</span>', unsafe_allow_html=True)
                
                # Selection Row
                opt1, opt2, opt3 = st.columns(3)
                
                colors = [c.strip() for c in str(row.get('available_colors', 'Default')).split(',')]
                chosen_color = opt1.selectbox("Color", colors, key=f"c_{idx}")

                sizes = [s.strip() for s in str(row.get('available_sizes', 'N/A')).split(',')]
                chosen_size = opt2.selectbox("Size", sizes, key=f"s_{idx}")

                # --- THE QUANTITY FIX ---
                qty = opt3.number_input("Qty", min_value=1, value=1, key=f"q_{idx}")

                try:
                    base_price = float(row.get('price', 0)) * 1.05
                except:
                    base_price = 0
                
                total_price = (base_price if symbol == "₦" else (base_price / rate)) * qty
                st.markdown(f"<p class='price-text'>{symbol}{total_price:,.0f}</p>", unsafe_allow_html=True)
                
                if is_out:
                    st.link_button("🔔 Notify Me", f"https://wa.me/{WHATSAPP_NUMBER}?text=Notify%20me%20for%20{p_name}")
                else:
                    b1, b2 = st.columns(2)
                    b1.link_button("💳 Pay Now", FLUTTERWAVE_LINK, use_container_width=True)
                    
                    # WhatsApp message includes Quantity, Color, and Size
                    msg = f"I%20want%20to%20order:%0A-{p_name}%0A-Qty:%20{qty}%0A-Color:%20{chosen_color}%0A-Size:%20{chosen_size}"
                    b2.link_button("💬 Chat to Order", f"https://wa.me/{WHATSAPP_NUMBER}?text={msg}", use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("Could not load products. Please check your Google Sheet columns.")

# --- OTHER PAGES (RESTORED) ---
elif menu == "🏢 Merchant Catalog":
    st.header("Verified Partners")
    m_data = load_sheet_data(MERCHANTS_URL)
    if not m_data.empty:
        for _, row in m_data.iterrows():
            with st.expander(f"✅ {str(row.iloc[0]).upper()}"):
                st.write(f"**Niche:** {row.get('niche', 'General')}")
                st.markdown(f"[🚩 Report](https://wa.me/{WHATSAPP_NUMBER}?text=Report%20Merchant)")
else:
    st.info(f"Welcome to the {menu} section!")

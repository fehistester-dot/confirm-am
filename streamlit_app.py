import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. Page Configuration
st.set_page_config(page_title="ConfirmAm Marketplace", page_icon="🛡️", layout="wide")

# 2. CONFIG
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
        df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
        return df.dropna(how='all')
    except:
        return pd.DataFrame()

# 3. Styling
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    .product-card { background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #eee; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); position: relative; }
    .price-text { color: #1DA1F2; font-weight: 800; font-size: 1.8em; margin: 5px 0; }
    .vendor-tag { background: #e1f5fe; color: #01579b; font-size: 0.8em; padding: 4px 10px; border-radius: 20px; font-weight: bold; }
    .sale-badge { background: #ff4b4b; color: white; padding: 5px 12px; border-radius: 10px; font-weight: bold; font-size: 0.8em; }
    .stock-badge { color: #ff4b4b; font-weight: bold; border: 1px solid #ff4b4b; padding: 2px 8px; border-radius: 5px; font-size: 0.8em; }
    .character-header { display: flex; align-items: center; gap: 20px; background: white; padding: 15px; border-radius: 15px; border: 1px solid #eee; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.image(ZIMI_SIDEBAR, use_container_width=True)
currency = st.sidebar.selectbox("Display Currency", ["🇳🇬 NGN (Naira)", "🇺🇸 USD (Dollar)"])
rate, symbol = (1500, "₦") if "NGN" in currency else (1, "$")

menu = st.sidebar.radio("Navigate", ["🛍️ Shopping Mall", "🏢 Merchant Catalog", "🛡️ How Escrow Works", "📥 Apply to Sell", "📞 Contact Support"])

# --- SHOPPING MALL ---
if menu == "🛍️ Shopping Mall":
    st.markdown(f'<div class="character-header"><img src="{ZIMI_SIDEBAR}" width="100"><div><h1 style="margin:0; color:#1DA1F2;">ConfirmAm Mall</h1><p style="margin:0; color:#666;"><b>Captain Zimi:</b> "Fresh deals just landed! Check the badges for sales."</p></div></div>', unsafe_allow_html=True)
    
    data = load_sheet_data(PRODUCTS_URL)
    if not data.empty:
        search = st.text_input("🔍 Search products...", "").lower()
        if search: data = data[data['name'].str.lower().str.contains(search, na=False)]

        for idx, row in data.iterrows():
            is_out = str(row.get('status', '')).lower() == "out of stock"
            is_sale = str(row.get('on_sale', '')).lower() == "yes"
            
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            col1, col2 = st.columns([1, 1.5])
            
            with col1:
                st.image(row.get('image_url', ''), use_container_width=True)

            with col2:
                # Badge Row
                badge_html = f'<span class="sale-badge">🔥 SALE</span> ' if is_sale else ""
                badge_html += f'<span class="stock-badge">🚫 SOLD OUT</span>' if is_out else ""
                st.markdown(badge_html, unsafe_allow_html=True)
                
                st.markdown(f"## {row.get('name', 'Product')}")
                st.markdown(f'<span class="vendor-tag">👤 Vendor: {row.get('seller', 'Verified')}</span>', unsafe_allow_html=True)
                
                s_col1, s_col2, s_col3 = st.columns(3)
                sel_color = s_col1.selectbox("Color", [c.strip() for c in str(row.get('available_colors', 'Default')).split(',')], key=f"c{idx}")
                sel_size = s_col2.selectbox("Size", [s.strip() for s in str(row.get('available_sizes', 'N/A')).split(',')], key=f"s{idx}")
                sel_qty = s_col3.number_input("Qty", 1, 10, 1, key=f"q{idx}")

                raw_price = float(row.get('price', 0)) * 1.05
                total = (raw_price if symbol == "₦" else (raw_price / rate)) * sel_qty
                st.markdown(f"<div class='price-text'>{symbol}{total:,.0f}</div>", unsafe_allow_html=True)

                b_col1, b_col2 = st.columns(2)
                if is_out:
                    st.warning("This item is currently out of stock.")
                    st.link_button("🔔 Notify Me on WhatsApp", f"https://wa.me/{WHATSAPP_NUMBER}?text=Notify%20me%20when%20{row.get('name')}%20is%20back!", use_container_width=True)
                else:
                    with b_col1: st.link_button("💳 Instant Buy", FLUTTERWAVE_LINK, use_container_width=True)
                    with b_col2:
                        msg = f"I want to order:\n*{row.get('name')}*\nColor: {sel_color}\nSize: {sel_size}\nQty: {sel_qty}"
                        st.link_button("💬 Chat to Order", f"https://wa.me/{WHATSAPP_NUMBER}?text={requests.utils.quote(msg)}", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else: st.info("Zimi is restocking...")

# --- OTHER PAGES (UNCHANGED) ---
elif menu == "🏢 Merchant Catalog":
    st.title("Verified Merchants")
    m_data = load_sheet_data(MERCHANTS_URL)
    if not m_data.empty:
        for _, row in m_data.iterrows():
            with st.expander(f"✅ {str(row.iloc[0]).upper()}"):
                st.write(f"**Niche:** {row.get('niche', 'General')}")
                st.write(f"**Socials:** {row.get('socials', 'Verified')}")

elif menu == "🛡️ How Escrow Works":
    st.header("The Zimi Guarantee")
    st.write("1. Secure Payment | 2. Verification | 3. Release")

elif menu == "📥 Apply to Sell":
    with st.form("Apply"):
        st.text_input("Business Name")
        if st.form_submit_button("Submit Application"): st.success("Success!")

elif menu == "📞 Contact Support":
    st.link_button("Chat with Support", f"https://wa.me/{WHATSAPP_NUMBER}")

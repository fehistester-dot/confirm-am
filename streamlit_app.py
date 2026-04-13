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
WHATSAPP_NUMBER = "2349136533490"  # Your New Official Number

PRODUCTS_URL = f"https://docs.google.com/spreadsheets/d/{PRODUCT_SHEET_ID}/export?format=csv&gid=0"
MERCHANTS_URL = f"https://docs.google.com/spreadsheets/d/{MERCHANT_SHEET_ID}/export?format=csv&gid=0"
FLUTTERWAVE_LINK = "https://flutterwave.com/pay/ctppxixgdke7"

# --- ZIMI IMAGE LINKS ---
ZIMI_SIDEBAR = "https://i.postimg.cc/9QdS9nRv/Gemini-Generated-Image-5wc5485wc5485wc5-removebg-preview.png"

# --- THE MASTER KEY CONNECTION ---
def load_sheet_data(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        df = pd.read_csv(StringIO(response.text), on_bad_lines='skip')
        df.columns = [c.strip().lower() for c in df.columns]
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
    .report-text { font-size: 0.8em; color: #ff4b4b; text-decoration: none; font-weight: bold; }
    
    div[data-testid="stForm"] {
        border: 1px solid #eee; padding: 20px; border-radius: 15px; background-color: white;
    }
    .safety-card {
        background-color: #f0f9ff; padding: 20px; border-left: 5px solid #1DA1F2; border-radius: 10px; margin-bottom: 15px;
    }
    .character-header {
        display: flex; align-items: center; gap: 20px; background: white; padding: 15px; border-radius: 15px; border: 1px solid #eee; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR & GLOBAL SETTINGS ---
st.sidebar.image(ZIMI_SIDEBAR, use_container_width=True)
st.sidebar.markdown(f"**Chat with Zimi:** [Click Here](https://wa.me/{WHATSAPP_NUMBER})")
currency = st.sidebar.selectbox("Display Currency", ["🇳🇬 NGN (Naira)", "🇺🇸 USD (Dollar)"])
rate = 1500 
symbol = "₦" if "NGN" in currency else "$"

st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigate", ["🛍️ Shopping Mall", "🏢 Merchant Catalog", "🛡️ How Escrow Works", "📥 Apply to Sell", "📢 Advertise Product", "📞 Contact Support"])

# --- 1. SHOPPING MALL (UPDATED WITH SELECTIONS) ---
if menu == "🛍️ Shopping Mall":
    st.markdown(f"""
        <div class="character-header">
            <img src="{ZIMI_SIDEBAR}" width="100">
            <div>
                <h1 style="margin:0; color:#1DA1F2;">ConfirmAm Mall</h1>
                <p style="margin:0; color:#666;"><b>Captain Zimi:</b> "Safe shopping is the only way to shop! Select your options below."</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    search_query = st.text_input("🔍 Search for products, brands, or categories...", "").lower()

    data = load_sheet_data(PRODUCTS_URL)
    if not data.empty:
        if search_query:
            data = data[data['name'].str.lower().str.contains(search_query, na=False)]

        for idx, row in data.iterrows():
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            col1, col2 = st.columns([1, 2])
            
            with col1:
                img_url = row.get('image_url', row.get('image', ''))
                try: st.image(img_url, use_container_width=True)
                except: st.warning("Image Loading...")

            with col2:
                st.markdown(f"### {row.get('name', 'Product')}")
                st.markdown(f'<span class="vendor-tag">👤 {row.get("seller", "Verified")}</span>', unsafe_allow_html=True)
                
                # --- OPTIONS ROW ---
                opt1, opt2, opt3 = st.columns(3)
                
                # Colors
                colors_raw = str(row.get('available_colors', 'Default'))
                color_list = [c.strip() for c in colors_raw.split(',')]
                chosen_color = opt1.selectbox("Color", color_list, key=f"col_{idx}")

                # Sizes
                sizes_raw = str(row.get('available_sizes', 'N/A'))
                size_list = [s.strip() for s in sizes_raw.split(',')]
                chosen_size = opt2.selectbox("Size", size_list, key=f"sz_{idx}")

                # Quantity
                qty = opt3.number_input("Qty", min_value=1, max_value=10, value=1, key=f"qty_{idx}")

                # Price Logic
                try: price = float(row.get('price', 0)) * 1.05
                except: price = 0
                display_price = (price if symbol == "₦" else (price / rate)) * qty

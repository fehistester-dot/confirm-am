import streamlit as st
import pandas as pd

# 1. Page Configuration (Logo in browser tab)
st.set_page_config(
    page_title="ConfirmAm Marketplace", 
    page_icon="https://i.postimg.cc/mD3WvH5n/Confirm-Am-Logo-Tick.png",
    layout="wide"
)

# 2. Your Live Payment Link
FLUTTERWAVE_LINK = "https://flutterwave.com/pay/ctppxixgdke7"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Amh_WmVwXCeZhc0h6NesZhBuGZAT0Ch60PuH-BF3xVE/export?format=csv"

# 3. Design & Styling
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    .product-card {
        background-color: white;
        padding: 15px;
        border-radius: 15px;
        border: 1px solid #eee;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .price-text { color: #1DA1F2; font-weight: 800; font-size: 1.3em; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: LOGO & IDENTITY ---
st.sidebar.image("https://i.postimg.cc/mD3WvH5n/Confirm-Am-Logo-Tick.png", use_container_width=True)
st.sidebar.markdown("<h2 style='text-align:center; color:#1DA1F2;'>ConfirmAm</h2>", unsafe_allow_html=True)
st.sidebar.info("Verified Marketplace & Escrow Service 🛡️")

# Contact Support (Replacement for 'ghost' site checks)
st.sidebar.link_button("💬 Chat with Support", "https://wa.me/2347046481507") 
st.sidebar.markdown("---")

menu = st.sidebar.radio("Navigation", ["🛍️ Shopping Mall", "📥 Merchant Portal", "🛡️ Safety & Escrow"])

# --- OPTION 1: THE SHOPPING MALL ---
if menu == "🛍️ Shopping Mall":
    st.markdown("<h1 style='text-align:center;'>ConfirmAm Mall</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#888;'>Safe. Secure. Verified.</p>", unsafe_allow_html=True)
    
    try:
        data = pd.read_csv(SHEET_URL)
        data.columns = data.columns.str.strip().str.lower()
        
        cols = st.columns(2)
        for i, row in data.iterrows():
            with cols[i % 2]:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                
                # Image Display
                if 'image_url' in row and pd.notnull(row['image_url']):
                    st.image(row['image_url'], use_container_width=True)
                
                # Verified Badge Logic
                is_v = str(row.get('verified', '')).strip().upper() == "TRUE"
                badge = '<span style="color:#1DA1F2;"> ☑️ Verified</span>' if is_v else ""
                
                # Product Info
                st.markdown(f"""
                    <p style="font-size:0.75em; color:#666; margin-bottom:2px;">{row.get('seller', 'Vendor')} {badge}</p>
                    <b style="font-size:1.2em;">{row.get('name', 'Luxury Item')}</b>
                    <p class="price-text">₦{row.get('price', 0):,}</p>
                """, unsafe_allow_html=True)
                
                # THE LIVE PAYMENT BUTTON
                st.link_button("Buy with Escrow", FLUTTERWAVE_LINK, use_container_width=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error("Catalog update in progress...")

# --- OPTION 2: MERCHANT PORTAL ---
elif menu == "📥 Merchant Portal":
    st.title("Partner with ConfirmAm")
    st.write("Join the circle of verified Nigerian fashion vendors.")
    
    with st.form("merchant_form"):
        brand = st.text_input("Brand Name")
        item = st.text_input("Product Name")
        price = st.number_input("Price (₦)")
        img_link = st.text_input("Image Link (Direct JPG)")
        
        if st.form_submit_button("Submit for QC Review"):
            st.success("Sent! We review submissions every night at 8:00 PM.")
            st.code(f"NEW, {item}, {price}, {brand}, FALSE, {img_link}")

# --- OPTION 3: SAFETY & TERMS ---
elif menu == "🛡️ Safety & Escrow":
    st.title("How ConfirmAm Protects You")
    st.markdown("""
    ### 🛡️ The Escrow Process
    1. **You Pay:** Money goes to ConfirmAm (not the vendor).
    2. **Vendor Ships:** We notify the vendor to send your item.
    3. **You Confirm:** Once you receive the item, you tell us.
    4. **We Release:** Only then is the vendor paid.
    
    *If the item never arrives or is the wrong size, you get your money back.*
    """)

import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="ConfirmAm", page_icon="🛡️", layout="wide")

# 2. THE "CLEAN LOOK" CODE (Hides Streamlit branding for visitors)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton {display:none;}
    .stApp { background-color: #fcfcfc; }
    .product-card {
        background-color: white;
        padding: 15px;
        border-radius: 15px;
        border: 1px solid #eee;
        margin-bottom: 20px;
        text-align: center;
    }
    .price-text { color: #d4af37; font-weight: 800; font-size: 1.2em; }
    </style>
    """, unsafe_allow_html=True)

# 3. Your Database Link
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Amh_WmVwXCeZhc0h6NesZhBuGZAT0Ch60PuH-BF3xVE/export?format=csv"

# --- SIDEBAR NAVIGATION ---
st.sidebar.markdown("## 🛡️ ConfirmAm HQ")
st.sidebar.markdown("---")

# CHANGE THE NUMBER BELOW TO YOUR REAL WHATSAPP NUMBER
st.sidebar.link_button("Contact Support", "https://wa.me/2348000000000") 

menu = st.sidebar.radio("Main Menu", ["Shopping Mall", "Merchant Portal", "Safety & Terms", "Install App"])

# --- OPTION 1: THE SHOPPING MALL ---
if menu == "Shopping Mall":
    st.markdown("<h1 style='text-align:center; color:#000;'>ConfirmAm Mall</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#888;'>Secure Escrow Protection Enabled 🛡️</p>", unsafe_allow_html=True)
    
    try:
        data = pd.read_csv(SHEET_URL)
        data.columns = data.columns.str.strip().str.lower()
        
        cols = st.columns(2)
        for i, row in data.iterrows():
            with cols[i % 2]:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)
                if 'image_url' in row and pd.notnull(row['image_url']):
                    st.image(row['image_url'], use_container_width=True)
                
                is_v = str(row.get('verified', '')).strip().upper() == "TRUE"
                badge = " ☑️" if is_v else ""
                
                st.markdown(f"**{row.get('name', 'Luxury Item')}**")
                st.markdown(f"<p class='price-text'>₦{row.get('price', 0):,}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size:0.8em; color:#666;'>Vendor: {row.get('seller', 'Vendor')}{badge}</p>", unsafe_allow_html=True)
                
                st.button("Secure Purchase", key=f"btn_{i}", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
    except:
        st.warning("Updating catalog... please refresh in a minute.")

# --- OPTION 2: THE MERCHANT PORTAL ---
elif menu == "Merchant Portal":
    st.title("📤 Merchant Application")
    st.info("🕒 **Review Schedule:** ConfirmAm reviews all submissions daily at **8:00 PM WAT**.")
    
    with st.form("merchant_upload"):
        v_brand = st.text_input("Brand Name")
        p_title = st.text_input("Product Title")
        p_amt = st.number_input("Listing Price (₦)", min_value=0)
        p_link = st.text_input("Direct Image Link (.jpg or .png)")
        
        if st.form_submit_button("Submit to ConfirmAm"):
            if v_brand and p_title and p_link:
                st.success("✅ Submission Received!")
                st.code(f"NEW, {p_title}, {p_amt}, {v_brand}, FALSE, {p_link}", language="text")
                st.write("Copy the code above and send to ConfirmAm Support.")
            else:
                st.error("Please fill in all fields.")

# --- OPTION 3: SAFETY & TERMS ---
elif menu == "Safety & Terms":
    st.title("🛡️ Escrow & Safety Policy")
    st.write("""
    ConfirmAm is a registered Marketplace and Retail Service Provider.
    
    1. **Escrow Protection:** Payment is held securely until you confirm delivery.
    2. **Verified Vendors:** Blue ticks (☑️) indicate vendors vetted by our team.
    3. **Refunds:** Disputes must be raised within 24 hours of delivery.
    """)

# --- OPTION 4: INSTALL APP ---
elif menu == "Install App":
    st.title("📲 Install ConfirmAm")
    st.markdown("""
    **iPhone (Safari):** Tap 'Share' > 'Add to Home Screen'.
    
    **Android (Chrome):** Tap the 3 dots > 'Install App'.
    """)

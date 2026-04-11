import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="ConfirmAm", page_icon="🛡️", layout="wide")

# 2. Your Database Link
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Amh_WmVwXCeZhc0h6NesZhBuGZAT0Ch60PuH-BF3xVE/export?format=csv"

# 3. Professional Styling
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
    }
    .price-text { color: #d4af37; font-weight: 800; font-size: 1.2em; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.image("https://img.icons8.com/ios-filled/100/d4af37/shield.png", width=50) # Just a placeholder gold shield
menu = st.sidebar.radio("Main Menu", ["Shopping Mall", "Merchant Portal", "Install App"])

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
                
                # Image Display
                if 'image_url' in row and pd.notnull(row['image_url']):
                    st.image(row['image_url'], use_container_width=True)
                else:
                    st.markdown('<div style="height:150px; background:#f9f9f9; border-radius:10px;"></div>', unsafe_allow_html=True)
                
                # Verified Status
                is_v = str(row.get('verified', '')).strip().upper() == "TRUE"
                badge = '<span style="color:#1DA1F2;"> ☑️</span>' if is_v else ""
                
                st.markdown(f"""
                    <div style="margin-top:10px;">
                        <p style="font-size:0.7em; color:#666; margin:0; text-transform:uppercase;">{row.get('seller', 'Vendor')} {badge}</p>
                        <b style="font-size:1.1em; color:#111;">{row.get('name', 'Luxury Item')}</b>
                        <p class="price-text">₦{row.get('price', 0):,}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.button("Secure Purchase", key=f"btn_{i}", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
    except:
        st.warning("Refreshing catalog... please wait.")

# --- OPTION 2: THE MERCHANT PORTAL ---
elif menu == "Merchant Portal":
    st.title("📥 Merchant Application")
    st.write("Submit your product details below. **ConfirmAm Quality Control** will review your submission.")
    
    with st.form("merchant_upload"):
        st.subheader("Product Details")
        v_brand = st.text_input("Registered Brand Name")
        p_title = st.text_input("Product Title")
        p_amt = st.number_input("Listing Price (₦)", min_value=0)
        p_link = st.text_input("Direct Image Link (from PostImages.org)")
        
        st.divider()
        st.write("By submitting, you agree to the ConfirmAm 48-hour Escrow Release policy.")
        
        if st.form_submit_button("Submit to ConfirmAm"):
            if v_brand and p_title and p_link:
                st.success("✅ Submission Received! ConfirmAm will review and sync your product shortly.")
                # Generating the easy copy-paste line for you
                formatted_data = f"NEW_ID, {p_title}, {p_amt}, {v_brand}, FALSE, {p_link}"
                st.info("Merchant Code (Copy & Send to ConfirmAm Support):")
                st.code(formatted_data, language="text")
            else:
                st.error("Please fill in all fields.")

# --- OPTION 3: INSTALL APP ---
elif menu == "Install App":
    st.title("📲 Install ConfirmAm")
    st.markdown("""
    Add ConfirmAm to your home screen for instant access to secure shopping.
    
    **iPhone (Safari):**
    1. Tap the **Share** icon (square with arrow).
    2. Select **'Add to Home Screen'**.
    
    **Android (Chrome):**
    1. Tap the **3 vertical dots**.
    2. Select **'Install App'** or **'Add to Home Screen'**.
    """)

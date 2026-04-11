import streamlit as st
import pandas as pd

# 1. Page Config
st.set_page_config(page_title="ConfirmAm", page_icon="🛍️", layout="wide")

# 2. Your Database Link
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Amh_WmVwXCeZhc0h6NesZhBuGZAT0Ch60PuH-BF3xVE/export?format=csv"

# 3. Custom Styling
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    .product-card {
        background-color: white;
        padding: 12px;
        border-radius: 15px;
        border: 1px solid #eee;
        margin-bottom: 20px;
    }
    .price-text { color: #d4af37; font-weight: 800; font-size: 1.2em; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
menu = st.sidebar.radio("Navigation", ["Shopping Mall", "Merchant Portal (Upload)", "How to Install App"])

# --- OPTION 1: THE SHOPPING MALL ---
if menu == "Shopping Mall":
    st.markdown("<h2 style='text-align:center;'>ConfirmAm Mall ✨</h2>", unsafe_allow_html=True)
    
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
                badge = "☑️" if is_v else ""
                
                st.markdown(f"""
                    <p style="font-size:0.7em; color:#888; margin:0;">{row.get('seller', 'Vendor')} {badge}</p>
                    <b style="font-size:1em;">{row.get('name', 'Item')}</b>
                    <p class="price-text">₦{row.get('price', 0):,}</p>
                """, unsafe_allow_html=True)
                st.button("Secure Order", key=f"btn_{i}", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
    except:
        st.info("Mall is being updated... refresh in 1 minute.")

# --- OPTION 2: THE MERCHANT PORTAL (The "Job Saver") ---
elif menu == "Merchant Portal (Upload)":
    st.title("📤 Vendor Upload Tool")
    st.info("Fill this out to list your product. Fehi will review and add the 'Verified' badge if approved.")
    
    with st.form("vendor_form"):
        v_name = st.text_input("Brand Name")
        p_name = st.text_input("Product Name")
        p_price = st.number_input("Price (₦)", min_value=0)
        p_img = st.text_input("Photo Link (Direct Link from PostImages.org)")
        
        submitted = st.form_submit_button("Submit for Review")
        if submitted:
            st.success("✅ Submitted! Your product will appear once Fehi syncs the sheet.")
            # FOR NOW: This gives you the text to copy-paste. 
            # SOON: We can use 'st_gsheets_connection' to automate the write-back!
            st.code(f"{p_name}, {p_price}, {v_name}, FALSE, {p_img}", language="text")
            st.write("👆 Copy this line and send it to Fehi to be added instantly!")

# --- OPTION 3: INSTALL INSTRUCTIONS ---
elif menu == "How to Install App":
    st.title("📲 Save to Home Screen")
    st.markdown("""
    ### For iPhone (Safari):
    1. Tap the **Share** button (Square with up arrow).
    2. Scroll down and tap **'Add to Home Screen'**.
    3. Tap **Add** in the top right.
    
    ### For Android (Chrome):
    1. Tap the **3 dots** in the top right corner.
    2. Tap **'Install App'** or **'Add to Home Screen'**.
    """)

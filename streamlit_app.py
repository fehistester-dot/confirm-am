import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="ConfirmAm", page_icon="🛡️", layout="wide")

# 2. Database (Replace with your link)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Amh_WmVwXCeZhc0h6NesZhBuGZAT0Ch60PuH-BF3xVE/export?format=csv"

# --- SIDEBAR ---
st.sidebar.title("🛡️ ConfirmAm")
st.sidebar.markdown("The Gold Standard for Secure Fashion.")

# WhatsApp Support (Crucial for Trust)
st.sidebar.link_button("Contact Support", "https://wa.me/234XXXXXXXXXX") 

menu = st.sidebar.radio("Navigation", ["Shopping Mall", "Merchant Portal", "Safety & Escrow"])

# --- OPTION 1: SHOPPING MALL ---
if menu == "Shopping Mall":
    st.markdown("<h1 style='text-align:center;'>ConfirmAm Mall</h1>", unsafe_allow_html=True)
    
    try:
        data = pd.read_csv(SHEET_URL)
        data.columns = data.columns.str.strip().str.lower()
        
        cols = st.columns(2)
        for i, row in data.iterrows():
            with cols[i % 2]:
                st.markdown('<div style="border:1px solid #eee; padding:15px; border-radius:15px; background:white; text-align:center; margin-bottom:20px;">', unsafe_allow_html=True)
                if 'image_url' in row and pd.notnull(row['image_url']):
                    st.image(row['image_url'], use_container_width=True)
                
                # Verified Badge Logic
                is_v = str(row.get('verified', '')).strip().upper() == "TRUE"
                badge = " ☑️" if is_v else ""
                
                st.markdown(f"### {row.get('name', 'Luxury Item')}")
                st.markdown(f"<p style='color:#d4af37; font-size:1.3em; font-weight:bold;'>₦{row.get('price', 0):,}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:#888; font-size:0.8em;'>Vendor: {row.get('seller', 'Store')}{badge}</p>", unsafe_allow_html=True)
                
                st.button("Secure Order", key=f"buy_{i}", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
    except:
        st.info("The Mall is being restocked. Please refresh in a moment.")

# --- OPTION 2: MERCHANT PORTAL ---
elif menu == "Merchant Portal":
    st.title("📤 Vendor Submission")
    st.write("Join the elite circle of ConfirmAm verified vendors.")
    st.info("Review Schedule: Submissions are batched daily at 8:00 PM WAT.")
    
    with st.form("merchant_form"):
        v_name = st.text_input("Brand Name")
        p_name = st.text_input("Product Name")
        p_price = st.number_input("Price (₦)", min_value=0)
        p_img = st.text_input("Direct Image Link (ends in .jpg or .png)")
        
        if st.form_submit_button("Submit Product"):
            st.success("Success! Copy the code below and send it to the ConfirmAm admin.")
            st.code(f"NEW, {p_name}, {p_price}, {v_name}, FALSE, {p_img}")

# --- OPTION 3: SAFETY & ESCROW (Compliance Header) ---
elif menu == "Safety & Escrow":
    st.title("🛡️ Our Escrow Protection")
    st.write("""
    ConfirmAm is built on trust. Here is how we protect you:
    - **Payments:** All funds stay in our secure vault until you confirm delivery.
    - **Verification:** We manually vet every 'Blue Tick' vendor.
    - **Disputes:** Not as described? Contact support within 24 hours for a resolution.
    """)
    st.divider()
    st.markdown("<p style='font-size:0.8em; color:#999;'>ConfirmAm is a registered Marketplace and Retail Service Provider.</p>", unsafe_allow_html=True)

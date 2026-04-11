import streamlit as st
import uuid
from PIL import Image

# 1. Page Configuration & Professional Styling
st.set_page_config(page_title="ConfirmAm Escrow", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 25px; height: 3em; background-color: #007bff; color: white; font-weight: bold; }
    .deal-card { padding: 20px; border-radius: 15px; background-color: white; border: 1px solid #e0e0e0; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Initialize our "Database" (Temporary)
if 'deals' not in st.session_state:
    st.session_state.deals = {}

st.title("🛡️ ConfirmAm Escrow")
st.write("Secure 'Pay Before Delivery' transactions for Nigerian Social Commerce.")

tab1, tab2, tab3 = st.tabs(["📤 Create Deal (Seller)", "📥 Complete Deal (Buyer)", "ℹ️ How it Works"])

# --- SELLER TAB ---
with tab1:
    st.header("Start a New Transaction")
    
    with st.container():
        item_name = st.text_input("Item Name", placeholder="e.g. Vintage Silk Two-Piece")
        item_img = st.file_uploader("Upload Item Photo (Optional)", type=['jpg', 'png', 'jpeg'])
        
        # The "Invisible Fee" Math
        raw_price = st.number_input("Selling Price (₦)", min_value=100, step=500, value=5000)
        total_fee = raw_price * 0.05
        seller_payout = raw_price - total_fee
        
        st.info(f"💡 **Buyer pays exactly ₦{raw_price:,.2f}**. You receive ₦{seller_payout:,.2f} after our 5% security fee.")
        
        seller_bank = st.text_input("Your Bank Account Details (for payout)")
        
        if st.button("Create Secure Deal Link"):
            if item_name and seller_bank:
                deal_id = str(uuid.uuid4())[:8].upper()
                st.session_state.deals[deal_id] = {
                    "item": item_name,
                    "price": raw_price,
                    "payout": seller_payout,
                    "status": "Awaiting Payment",
                    "image": item_img,
                    "bank": seller_bank
                }
                st.success(f"Deal Created! ID: {deal_id}")
                
                # WhatsApp Shortcut
                wa_msg = f"Hello! I've created a secure deal for the {item_name} on ConfirmAm. Use ID: {deal_id} at confirmam-fehi.streamlit.app to pay safely."
                st.markdown(f"[📲 Send Deal to Buyer via WhatsApp](https://wa.me/?text={wa_msg.replace(' ', '%20')})")
            else:
                st.warning("Please fill in the Item Name and Bank details.")

# --- BUYER TAB ---
with tab2:
    st.header("Secure Your Purchase")
    search_id = st.text_input("Enter the 8-digit Deal ID").upper()
    
    if search_id in st.session_state.deals:
        d = st.session_state.deals[search_id]
        
        with st.expander("📦 View Deal Details", expanded=True):
            if d['image']:
                st.image(d['image'], width=300)
            st.subheader(d['item'])
            st.metric("Amount to Pay", f"₦{d['price']:,.2f}")
            st.write(f"**Current Status:** {d['status']}")
            
            # Progress Bar for trust
            steps = {"Awaiting Payment": 0, "Paid (In Escrow)": 50, "Shipped": 75, "Completed": 100}
            st.progress(steps.get(d['status'], 0))

        if d['status'] == "Awaiting Payment":
            if st.button("Confirm Payment (I have sent the ₦)"):
                d['status'] = "Paid (In Escrow)"
                st.rerun()
        
        elif d['status'] == "Paid (In Escrow)":
            st.success("✅ Money is secured in the ConfirmAm Vault.")
            if st.button("Mark as Shipped (Seller Only)"):
                d['status'] = "Shipped"
                st.rerun()
                
        elif d['status'] == "Shipped":
            st.warning("🚚 Item is on the way!")
            if st.button("I have Received my Item (Release Funds)"):
                d['status'] = "Completed"
                st.balloons()
                st.rerun()
                
        elif d['status'] == "Completed":
            st.success("Transaction Finished. Funds are being processed to the seller.")
    
    elif search_id:
        st.error("Deal ID not found. Check with the seller.")

# --- HELP TAB ---
with tab3:
    st.header("Why use ConfirmAm?")
    st.write("**For Buyers:** No more 'Pay before delivery' scams. We hold your money until you touch the item.")
    st.write("**For Sellers:** Stop being ghosted by 'Pay on Delivery' buyers. Know the money is secured before you ship.")
    st.divider()
    st.caption("ConfirmAm Charge: 5% flat fee (taken from the final payout).")

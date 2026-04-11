import streamlit as st
import uuid

# Set page style
st.set_page_config(page_title="ConfirmAm", page_icon="✅")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #007bff; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #f0f2f6; border-radius: 10px 10px 0 0; padding: 10px 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("✅ ConfirmAm Escrow")
st.write("The safest way to 'Pay Before Delivery' in Nigeria.")

# Initialize storage for the session
if 'deals' not in st.session_state:
    st.session_state.deals = {}

tab1, tab2, tab3 = st.tabs(["I am a Seller", "I am a Buyer", "Policy & Help"])

with tab1:
    st.header("Create a Secure Deal")
    item_name = st.text_input("What are you selling?", placeholder="e.g. Modest 2-Piece Set")
    base_price = st.number_input("Item Price (₦)", min_value=100, step=500)
    
    # Calculation (2.5% for Buyer + 2.5% for Seller = 5% total)
    fee_per_side = base_price * 0.025
    buyer_total = base_price + fee_per_side
    seller_receives = base_price - fee_per_side
    
    st.info(f"📊 **Fee Breakdown (5% Total):**")
    st.write(f"* Buyer pays: **₦{buyer_total:,.2f}**")
    st.write(f"* You receive: **₦{seller_receives:,.2f}** after 2.5% service fee.")
    
    seller_bank = st.text_input("Your Bank Account (for your payout)")
    
    if st.button("Generate Secure Deal ID"):
        if item_name and seller_bank:
            deal_id = str(uuid.uuid4())[:6].upper()
            st.session_state.deals[deal_id] = {
                "item": item_name,
                "price": buyer_total,
                "seller_net": seller_receives,
                "status": "Awaiting Payment",
                "bank": seller_bank
            }
            st.success(f"Deal Created! Share this ID with your buyer: **{deal_id}**")
        else:
            st.error("Please fill in all details before generating the ID.")

with tab2:
    st.header("Verify & Pay")
    search_id = st.text_input("Enter the ConfirmAm ID received from Seller").upper()
    
    if search_id in st.session_state.deals:
        deal = st.session_state.deals[search_id]
        st.info(f"**Item:** {deal['item']} | **Total to Pay:** ₦{deal['price']:,.2f}")
        
        if deal['status'] == "Awaiting Payment":
            if st.button("Pay into Secure Vault"):
                deal['status'] = "Money Secured"
                st.success("Payment Received! ConfirmAm is now holding the funds safely.")
        
        elif deal['status'] == "Money Secured":
            st.warning("⚠️ Money is held in Escrow.")
            if st.button("I Have Received My Item (Release Funds)"):
                deal['status'] = "Completed"
                st.balloons()
                st.success(f"Funds released! ₦{deal['seller_net']:,.2f} is being sent to the seller.")
    elif search_id:
        st.error("Deal ID not found. Please check with the seller.")

with tab3:
    st.header("Trust & Safety Policy")
    st.write("""
    **1. Security Fee:** We charge 2.5% to both parties to keep transactions safe.
    **2. Refund Policy:** If the seller fails to ship or the item is wrong/damaged, you get a refund (minus the 2.5% service fee).
    **3. Disputes:** Our team will review photos/videos from both sides to resolve issues fairly.
    """)
    st.link_button("Chat with Support", "https://wa.me/2340000000000") # Swap the 0s for your number!

st.markdown("---")
st.caption("ConfirmAm: Safety for Buyers. Growth for Sellers.")

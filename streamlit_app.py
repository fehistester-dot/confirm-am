import streamlit as st
import uuid

# Set page style
st.set_page_config(page_title="ConfirmAm", page_icon="✅")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #007bff; color: white; height: 3em; font-weight: bold;}
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
    item_name = st.text_input("What are you selling?", placeholder="e.g. Handkerchief Skirt Set")
    display_price = st.number_input("Price for the Buyer (₦)", min_value=100, step=500)
    
    # Logic: 5% total is taken from the Display Price
    total_fee = display_price * 0.05
    seller_receives = display_price - total_fee
    
    st.info(f"📊 **Price Summary:**")
    st.write(f"* Buyer pays exactly: **₦{display_price:,.2f}**")
    st.write(f"* You will receive: **₦{seller_receives:,.2f}**")
    st.caption(f"ConfirmAm takes a 5% service fee (₦{total_fee:,.2f}) to secure the deal.")
    
    seller_bank = st.text_input("Your Bank Account (for payout)")
    
    if st.button("Generate Secure Deal ID"):
        if item_name and seller_bank:
            deal_id = str(uuid.uuid4())[:6].upper()
            st.session_state.deals[deal_id] = {
                "item": item_name,
                "price": display_price,
                "seller_net": seller_receives,
                "status": "Awaiting Payment",
                "bank": seller_bank
            }
            st.success(f"Deal Created! Share this ID with your buyer: **{deal_id}**")

with tab2:
    st.header("Secure Payment")
    search_id = st.text_input("Enter the Deal ID from your Seller").upper()
    
    if search_id in st.session_state.deals:
        deal = st.session_state.deals[search_id]
        st.info(f"**Item:** {deal['item']}")
        st.metric("Amount to Pay", f"₦{deal['price']:,.2f}")
        
        if deal['status'] == "Awaiting Payment":
            if st.button("Pay into Secure Vault"):
                deal['status'] = "Money Secured"
                st.success("Payment Received! ConfirmAm is now holding the money safely.")
        
        elif deal['status'] == "Money Secured":
            st.warning("⚠️ Money is held by ConfirmAm.")
            if st.button("I Have Received My Item (Release Funds)"):
                deal['status'] = "Completed"
                st.balloons()
                st.success(f"Funds released! ₦{deal['seller_net']:,.2f} is being sent to the seller.")
    elif search_id:
        st.error("Invalid ID.")

with tab3:
    st.header("Trust & Safety")
    st.write("**Why use ConfirmAm?**")
    st.write("1. **No Scams:** We hold the money until the buyer confirms delivery.")
    # Add your WhatsApp number below by replacing the 0000000000
    st.link_button("Chat with Support", "https://wa.me/2340000000000")

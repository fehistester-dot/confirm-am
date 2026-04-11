import streamlit as st
import uuid

# Set page style
st.set_page_config(page_title="ConfirmAm", page_icon="✅")

st.title("✅ ConfirmAm Escrow")
st.write("The safest way to 'Pay Before Delivery' in Nigeria.")

# Initialize storage
if 'deals' not in st.session_state:
    st.session_state.deals = {}

tab1, tab2, tab3 = st.tabs(["I am a Seller", "I am a Buyer", "Policy & Help"])

with tab1:
    st.header("Create a Secure Deal")
    item_name = st.text_input("What are you selling?", placeholder="e.g. Modest 2-Piece Set")
    base_price = st.number_input("Item Price (₦)", min_value=100, step=500)
    
    # Calculation (2.5% each side = 5% total)
    fee_per_side = base_price * 0.025
    buyer_total = base_price + fee_per_side
    seller_receives = base_price - fee_per_side
    
    st.warning(f"📊 **Fee Breakdown (5% Total):**")
    st.write(f"* Buyer pays: **₦{buyer_total:,.2f}** (Price + 2.5% safety fee)")
    st.write(f"* You receive: **₦{seller_receives:,.2f}** (Price - 2.5% service fee)")
    
    seller_bank = st.text_input("Your Bank Account (for payout)")
    
    if st.button("Generate ConfirmAm ID"):
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

with tab2:
    st.header("Verify & Pay")
    search_id = st.text_input("Enter the ConfirmAm ID").upper()
    
    if search_id in st.session_state.deals:
        deal = st.session_state.deals[search_id]
        st.info(f"**Item:** {deal['item']} | **Total to Pay:** ₦{deal['price']:,.2f}")
        st.caption("This includes the 2.5% ConfirmAm protection fee.")
        
        if deal['status'] == "Awaiting Payment":
            if st.button("Pay into Secure Vault"):
                deal['status'] = "Money Secured"
                st.success("Payment Received! We are holding the money safely.")
        
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
    st.write("ConfirmAm charges a 2.5% fee to both parties to ensure a 100% scam-free environment.")
    # Add your WhatsApp number below by replacing the 07046481507
    st.link_button("Chat with Support", "https://wa.me/2340000000000")

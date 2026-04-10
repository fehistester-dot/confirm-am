import streamlit as st
import uuid

# Set page style
st.set_page_config(page_title="ConfirmAm", page_icon="✅")

st.title("✅ ConfirmAm Escrow")
st.write("The safest way to 'Pay Before Delivery' in Nigeria.")
st.markdown("---")

# Initialize storage for the app
if 'deals' not in st.session_state:
    st.session_state.deals = {}

tab1, tab2 = st.tabs(["I am a Seller", "I am a Buyer"])

with tab1:
    st.header("Create a Secure Deal")
    item_name = st.text_input("What are you selling?", placeholder="e.g. Vintage Silk Dress")
    amount = st.number_input("Amount (₦)", min_value=100)
    seller_bank = st.text_input("Your Bank Account (where we send the money)")
    
    if st.button("Generate ConfirmAm ID"):
        if item_name and seller_bank:
            deal_id = str(uuid.uuid4())[:6].upper()
            st.session_state.deals[deal_id] = {
                "item": item_name,
                "price": amount,
                "status": "Awaiting Payment",
                "bank": seller_bank
            }
            st.success(f"Deal Created! Share this ID with your buyer: **{deal_id}**")
        else:
            st.error("Please fill in all fields!")

with tab2:
    st.header("Verify & Pay")
    search_id = st.text_input("Enter the ConfirmAm ID from the seller").upper()
    
    if search_id in st.session_state.deals:
        deal = st.session_state.deals[search_id]
        st.info(f"**Item:** {deal['item']} | **Price:** ₦{deal['price']}")
        
        if deal['status'] == "Awaiting Payment":
            st.warning("Status: Awaiting your payment.")
            if st.button("Pay into ConfirmAm Vault"):
                deal['status'] = "Money Secured"
                st.success("Payment successful! We are holding the money. Tell the seller to ship!")
        
        elif deal['status'] == "Money Secured":
            st.success("✅ Money is Secure in our Vault.")
            st.write("Has the item been delivered exactly as described?")
            if st.button("YES, ConfirmAm & Release Funds"):
                deal['status'] = "Completed"
                st.balloons()
                st.success(f"Funds have been released to the seller! Thank you for using ConfirmAm.")
        
        elif deal['status'] == "Completed":
            st.info("This transaction is already completed.")
    elif search_id:
        st.error("Invalid ID. Please check with the seller.")

st.markdown("---")
st.caption("ConfirmAm: Building trust, one delivery at a time.")

import streamlit as st
import uuid

# 1. Page Config
st.set_page_config(page_title="ConfirmAm Marketplace", page_icon="🛡️", layout="wide")

# 2. Styling
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .product-card { background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #ddd; margin-bottom: 10px; text-align: center; }
    .payment-box { background-color: #e3f2fd; padding: 20px; border-radius: 15px; border: 2px dashed #007bff; }
    .stButton>button { border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Initialize Databases
if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'orders' not in st.session_state:
    st.session_state.orders = {}

st.title("🛡️ ConfirmAm Secure Marketplace")

tab1, tab2, tab3 = st.tabs(["🛒 Shop Arrivals", "📤 Seller: List Item", "💳 Buyer: My Payments"])

# --- TAB 1: SHOP ---
with tab1:
    st.header("Available for Secure Purchase")
    if not st.session_state.inventory:
        st.info("No items yet.")
    else:
        cols = st.columns(3)
        for idx, item in enumerate(st.session_state.inventory):
            with cols[idx % 3]:
                st.markdown(f'<div class="product-card"><h3>{item["name"]}</h3><h2>₦{item["price"]:,}</h2></div>', unsafe_allow_html=True)
                if item['image']: st.image(item['image'], use_container_width=True)
                
                if st.button(f"Buy Safely: {item['name']}", key=f"buy_{idx}"):
                    order_id = str(uuid.uuid4())[:6].upper()
                    st.session_state.orders[order_id] = {
                        "item": item['name'],
                        "price": item['price'],
                        "status": "Pending Payment",
                        "receipt": None
                    }
                    st.session_state.current_order = order_id
                    st.success(f"Order Created! Your Order ID is: {order_id}")
                    st.info("Go to the 'Buyer: My Payments' tab to pay.")

# --- TAB 2: SELLER ---
with tab2:
    st.header("Add to Catalog")
    with st.form("seller_form"):
        name = st.text_input("Product Name")
        price = st.number_input("Price (₦)", min_value=100)
        img = st.file_uploader("Upload Image", type=['jpg', 'png'])
        submitted = st.form_submit_button("Post to Shop")
        if submitted and name:
            st.session_state.inventory.append({"name": name, "price": price, "image": img})
            st.success("Item is live!")

# --- TAB 3: PAYMENT & PROTECTION ---
with tab3:
    st.header("Verify Your Payment")
    
    order_id_input = st.text_input("Enter your Order ID (from Tab 1)").upper()
    
    if order_id_input in st.session_state.orders:
        order = st.session_state.orders[order_id_input]
        
        st.write(f"### Order: {order['item']}")
        st.write(f"**Total Amount:** ₦{order['price']:,}")
        
        if order['status'] == "Pending Payment":
            st.markdown("""
            <div class="payment-box">
                <h4>🏦 Pay into the ConfirmAm Vault</h4>
                <p><strong>Bank:</strong> Zenith Bank</p>
                <p><strong>Account Name:</strong> ConfirmAm Escrow Services</p>
                <p><strong>Account Number:</strong> 1234567890</p>
                <p><i>Reference: Enter your Order ID in the transfer narration.</i></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("---")
            st.write("**Step 2: Upload Proof of Transfer**")
            receipt = st.file_uploader("Upload screenshot of bank receipt", type=['jpg', 'png', 'pdf'])
            
            if st.button("Submit Receipt for Verification"):
                if receipt:
                    order['receipt'] = receipt
                    order['status'] = "Verifying..."
                    st.rerun()
                else:
                    st.warning("Please upload a receipt first.")

        elif order['status'] == "Verifying...":
            st.warning("⏳ **Wait!** ConfirmAm is verifying your transfer. Sellers: DO NOT SHIP YET.")
            st.image(order['receipt'], caption="Submitted Receipt", width=200)
            
            # Simulated Admin Approval (For your testing)
            if st.button("Admin: Confirm Money is in Bank"):
                order['status'] = "Money Secured"
                st.rerun()

        elif order['status'] == "Money Secured":
            st.success("✅ **MONEY SECURED.** Seller, you can now ship the item safely.")
            st.write("Buyer: Once you receive the item, click the button below to release the money.")
            if st.button("Item Received (Release Money)"):
                order['status'] = "Completed"
                st.balloons()
    else:
        st.write("Enter an ID to view payment status.")

import streamlit as st
import uuid

# 1. Page Config & Professional Styling
st.set_page_config(page_title="ConfirmAm Marketplace", page_icon="🛍️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .product-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-bottom: 10px;
        text-align: center;
    }
    .stButton>button { border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Initialize the Global Marketplace Database
if 'inventory' not in st.session_state:
    st.session_state.inventory = []

st.title("🛍️ ConfirmAm Marketplace")
st.write("Browse unique items protected by Nigeria's safest escrow system.")

tab1, tab2, tab3 = st.tabs(["🛒 Browse Shop", "📤 Add Product (Seller)", "📦 My Orders"])

# --- TAB 1: BROWSE SHOP ---
with tab1:
    st.header("Latest Arrivals")
    if not st.session_state.inventory:
        st.info("The shop is currently empty. Sellers, start adding your products!")
    else:
        # Display items in a 3-column grid
        cols = st.columns(3)
        for idx, item in enumerate(st.session_state.inventory):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="product-card">
                    <h3>{item['name']}</h3>
                    <h2 style="color: #28a745;">₦{item['price']:,}</h2>
                </div>
                """, unsafe_allow_html=True)
                if item['image']:
                    st.image(item['image'], use_container_width=True)
                
                if st.button(f"Secure Buy: {item['name']}", key=f"buy_{idx}"):
                    st.session_state.selected_item = item
                    st.success(f"Proceeding to pay for {item['name']}! Go to 'My Orders' tab.")

# --- TAB 2: SELLER DASHBOARD ---
with tab2:
    st.header("List Your Products")
    with st.expander("Add New Item to Shop", expanded=True):
        new_name = st.text_input("Product Name", placeholder="e.g. Ankara Maxi Dress")
        new_price = st.number_input("Price (₦)", min_value=100, step=500)
        new_img = st.file_uploader("Product Image", type=['jpg', 'png', 'jpeg'])
        
        # Invisible Fee Logic for the Seller
        fee = new_price * 0.05
        payout = new_price - fee
        
        st.caption(f"Note: You will receive ₦{payout:,.2f} after the 5% security fee.")
        
        if st.button("List in Marketplace"):
            if new_name:
                product_data = {
                    "id": str(uuid.uuid4())[:8],
                    "name": new_name,
                    "price": new_price,
                    "image": new_img,
                    "status": "Available"
                }
                st.session_state.inventory.append(product_data)
                st.success(f"'{new_name}' is now live in the shop!")
                st.balloons()
            else:
                st.error("Please provide a product name.")

# --- TAB 3: BUYER ORDERS ---
with tab3:
    st.header("Your Secure Transactions")
    if 'selected_item' in st.session_state:
        item = st.session_state.selected_item
        st.write(f"### Complete Purchase: {item['name']}")
        st.metric("Total to Pay", f"₦{item['price']:,}")
        
        st.write("---")
        st.write("🛡️ **ConfirmAm Guarantee:** Your money is held in our vault until you confirm delivery.")
        
        if st.button("Confirm Payment & Secure Funds"):
            st.success("Payment Received! We've notified the seller to ship your item.")
            # Here we would normally move this to a 'Paid' status
    else:
        st.write("No active orders. Browse the shop to find something you love!")

import streamlit as st
import uuid

# 1. Page & Style Config
st.set_page_config(page_title="ConfirmAm", page_icon="✨", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .auth-box { max-width: 400px; padding: 30px; border-radius: 20px; background-color: #f8f9fa; margin: auto; border: 1px solid #eee; }
    .nav-btn { background-color: #000; color: #d4af37; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold; margin-bottom: 10px; }
    .product-card { border: 1px solid #eee; padding: 15px; border-radius: 15px; margin-bottom: 10px; text-align: center; }
    .stButton>button { border-radius: 50px; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. State Management
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = "Shop" # Default page
if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'orders' not in st.session_state:
    st.session_state.orders = {}

# --- LOGIN GATE ---
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="auth-box">', unsafe_allow_html=True)
        st.title("ConfirmAm 🔒")
        email = st.text_input("Email")
        pwd = st.text_input("Password", type="password")
        if st.button("Log In", use_container_width=True):
            if email and pwd:
                st.session_state.logged_in = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- THE MAIN INTERFACE ---
else:
    # 1. Premium Header
    st.markdown("""
        <div style="background-color:#000; color:#d4af37; padding:15px; border-radius:15px; text-align:center; margin-bottom:20px;">
            <h2 style="margin:0;">ConfirmAm Collection</h2>
        </div>
    """, unsafe_allow_html=True)

    # 2. CLEAR MOBILE NAVIGATION
    st.write("### 🧭 Main Menu")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🛍️ Shop"): st.session_state.page = "Shop"
    with c2:
        if st.button("📤 Sell"): st.session_state.page = "Sell"
    with c3:
        if st.button("🔒 Pay"): st.session_state.page = "Pay"

    st.divider()

    # 3. PAGE LOGIC
    if st.session_state.page == "Shop":
        st.subheader("The Marketplace")
        if not st.session_state.inventory:
            st.warning("Nothing here yet! Go to 'Sell' to add your first item.")
        else:
            for idx, item in enumerate(st.session_state.inventory):
                st.markdown(f'<div class="product-card"><h3>{item["name"]}</h3><h2>₦{item["price"]:,}</h2></div>', unsafe_allow_html=True)
                if item['image']: st.image(item['image'])
                if st.button(f"Buy Now", key=f"buy_{idx}"):
                    oid = str(uuid.uuid4())[:6].upper()
                    st.session_state.orders[oid] = item
                    st.session_state.last_oid = oid
                    st.success(f"Order {oid} Created! Go to 'Pay' menu.")

    elif st.session_state.page == "Sell":
        st.subheader("Add New Item")
        with st.form("seller_form", clear_on_submit=True):
            name = st.text_input("Item Name (e.g. Silk Set)")
            price = st.number_input("Price (₦)", min_value=100)
            img = st.file_uploader("Product Photo")
            if st.form_submit_button("Post Live"):
                if name:
                    st.session_state.inventory.append({"name": name, "price": price, "image": img})
                    st.success("Item is now live in the Shop!")
                else:
                    st.error("Please add a name.")

    elif st.session_state.page == "Pay":
        st.subheader("Secure Checkout")
        oid_in = st.text_input("Order ID", value=st.session_state.get('last_oid', '')).upper()
        if oid_in in st.session_state.orders:
            order = st.session_state.orders[oid_in]
            st.info(f"Paying for: {order['name']} - ₦{order['price']:,}")
            st.write("**Account:** 0123456789 | OPay | ConfirmAm")
            st.markdown('<a href="https://wa.me/2348012345678" target="_blank"><button style="width:100%; height:50px; background-color:#25D366; color:white; border:none; border-radius:50px; font-weight:bold;">VERIFY ON WHATSAPP</button></a>', unsafe_allow_html=True)
        else:
            st.write("Enter an Order ID to pay.")

    # 4. Sidebar Logout
    with st.sidebar:
        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.rerun()

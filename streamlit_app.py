import streamlit as st
import uuid

# 1. Page & Style Config
st.set_page_config(page_title="ConfirmAm Mall", page_icon="🏢", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .nav-btn { background-color: #000; color: #d4af37; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold; margin-bottom: 10px; }
    .product-card { border: 1px solid #eee; padding: 15px; border-radius: 15px; margin-bottom: 10px; background-color: #fff; }
    .seller-badge { background-color: #f0f0f0; color: #555; padding: 2px 8px; border-radius: 5px; font-size: 0.8em; font-weight: bold; }
    .stButton>button { border-radius: 50px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. State Management
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = "Shop"
if 'inventory' not in st.session_state:
    # Adding a few "Fake" sellers so you can see how the mall looks!
    st.session_state.inventory = [
        {"name": "Silk Wrap Dress", "price": 45000, "seller": "Fehi's Fashion", "image": None},
        {"name": "Men's Kaftan", "price": 35000, "seller": "Abuja Designs", "image": None}
    ]
if 'orders' not in st.session_state:
    st.session_state.orders = {}

# --- LOGIN GATE ---
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container():
        st.title("ConfirmAm 🔒")
        st.write("Sign in to enter the Marketplace")
        email = st.text_input("Email")
        pwd = st.text_input("Password", type="password")
        if st.button("Enter Mall", use_container_width=True):
            if email and pwd:
                st.session_state.logged_in = True
                st.rerun()

# --- THE MAIN MALL INTERFACE ---
else:
    st.markdown("""<div style="background-color:#000; color:#d4af37; padding:15px; border-radius:15px; text-align:center; margin-bottom:20px;">
        <h2 style="margin:0;">ConfirmAm Mall ✨</h2></div>""", unsafe_allow_html=True)

    # Navigation Buttons
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🛍️ Explore Mall"): st.session_state.page = "Shop"
    with c2:
        if st.button("📤 Start Selling"): st.session_state.page = "Sell"
    with c3:
        if st.button("🔒 My Orders"): st.session_state.page = "Pay"

    st.divider()

    # --- SHOP (THE MALL VIEW) ---
    if st.session_state.page == "Shop":
        st.subheader("All Trending Items")
        
        # Search filter (to help people find specific sellers)
        search = st.text_input("Search for a brand or item...", placeholder="e.g. Fehi's Fashion")
        
        for idx, item in enumerate(st.session_state.inventory):
            # Only show if it matches search
            if search.lower() in item['name'].lower() or search.lower() in item['seller'].lower():
                with st.container():
                    st.markdown(f"""
                    <div class="product-card">
                        <span class="seller-badge">👤 {item['seller']}</span>
                        <h3>{item['name']}</h3>
                        <h2 style="color:#d4af37;">₦{item['price']:,}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if item['image']: st.image(item['image'])
                    
                    if st.button(f"Buy from {item['seller']}", key=f"buy_{idx}"):
                        oid = str(uuid.uuid4())[:6].upper()
                        st.session_state.orders[oid] = item
                        st.session_state.last_oid = oid
                        st.success(f"Order {oid} created for {item['name']}!")

    # --- SELL (THE MERCHANT DASHBOARD) ---
    elif st.session_state.page == "Sell":
        st.subheader("Merchant Dashboard")
        st.write("List your products here to show them in the main mall.")
        with st.form("merchant_form", clear_on_submit=True):
            brand = st.text_input("Your Brand Name (e.g. Fehi's Fashion)")
            p_name = st.text_input("Product Name")
            p_price = st.number_input("Price (₦)", min_value=100)
            p_img = st.file_uploader("Product Photo")
            
            if st.form_submit_button("Launch Product"):
                if brand and p_name:
                    st.session_state.inventory.append({"name": p_name, "price": p_price, "seller": brand, "image": p_img})
                    st.balloons()
                    st.success(f"Congrats {brand}! Your item is now live in the mall.")
                else:
                    st.error("Brand name and Product name are required!")

    # --- PAY (THE SECURE ESCROW) ---
    elif st.session_state.page == "Pay":
        st.subheader("Secure Escrow Checkout")
        oid_in = st.text_input("Enter Order ID", value=st.session_state.get('last_oid', '')).upper()
        
        if oid_in in st.session_state.orders:
            order = st.session_state.orders[oid_in]
            st.info(f"Item: {order['name']} | Merchant: {order['seller']}")
            st.markdown(f"### Total: ₦{order['price']:,}")
            st.write("---")
            st.write("**Payment Details:** OPay | 0123456789 | ConfirmAm Services")
            st.warning("Note: Your money is held safely by ConfirmAm until you receive your order.")
            st.markdown('<button style="width:100%; height:50px; background-color:#25D366; color:white; border:none; border-radius:50px; font-weight:bold;">CONFIRM PAYMENT VIA WHATSAPP</button>', unsafe_allow_html=True)

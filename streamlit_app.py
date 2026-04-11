import streamlit as st
import uuid
from datetime import datetime

# 1. Page Configuration & Professional Styling
st.set_page_config(page_title="ConfirmAm | Official Mall", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stButton>button { border-radius: 50px; font-weight: bold; width: 100%; }
    .product-card { border: 1px solid #eee; padding: 15px; border-radius: 15px; background: #fff; margin-bottom: 15px; }
    .verified-tick { color: #1DA1F2; font-weight: bold; font-size: 0.9em; }
    .status-badge { padding: 5px 10px; border-radius: 20px; font-size: 0.8em; color: white; font-weight: bold; }
    .policy-box { background-color: #f1f1f1; padding: 20px; border-radius: 15px; border-left: 5px solid #d4af37; }
    </style>
    """, unsafe_allow_html=True)

# 2. State Management (Memory)
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "Mall"
if 'inventory' not in st.session_state:
    # Pre-loading Fehi's Fashion with a Verified Tick
    st.session_state.inventory = [
        {"id": "001", "name": "Luxury Silk Set", "price": 55000, "seller": "Fehi's Fashion", "verified": True}
    ]
if 'user_orders' not in st.session_state: st.session_state.user_orders = []

# --- 3. THE INTERFACE ---
if not st.session_state.logged_in:
    # (Login screen remains here for security)
    st.title("ConfirmAm 🔒")
    email = st.text_input("Email")
    pwd = st.text_input("Password", type="password")
    if st.button("Enter Secure Mall"):
        st.session_state.logged_in = True
        st.rerun()

else:
    # Top Navigation Bar
    st.markdown("""<div style="background-color:#000; color:#d4af37; padding:15px; border-radius:15px; text-align:center;">
        <h2 style="margin:0;">ConfirmAm Platform 🛡️</h2></div>""", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: 
        if st.button("🛍️ Mall"): st.session_state.page = "Mall"
    with col2: 
        if st.button("📦 Tracker"): st.session_state.page = "Tracker"
    with col3: 
        if st.button("📤 Sell"): st.session_state.page = "Sell"
    with col4: 
        if st.button("📜 Legal"): st.session_state.page = "Legal"

    st.divider()

    # --- MALL PAGE ---
    if st.session_state.page == "Mall":
        st.subheader("Explore Verified Vendors")
        for item in st.session_state.inventory:
            with st.container():
                tick = '<span class="verified-tick">✅ Verified</span>' if item['verified'] else ""
                st.markdown(f"""
                <div class="product-card">
                    <p style="margin:0;">{item['seller']} {tick}</p>
                    <h3 style="margin:0;">{item['name']}</h3>
                    <h2 style="color:#d4af37; margin:0;">₦{item['price']:,}</h2>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Secure Escrow Purchase", key=item['id']):
                    new_order = {
                        "oid": str(uuid.uuid4())[:6].upper(),
                        "item": item['name'],
                        "price": item['price'],
                        "status": "Pending Payment",
                        "date": datetime.now().strftime("%Y-%m-%d")
                    }
                    st.session_state.user_orders.append(new_order)
                    st.success(f"Order {new_order['oid']} created! Go to Tracker.")

    # --- TRACKER PAGE ---
    elif st.session_state.page == "Tracker":
        st.subheader("Your Active Orders")
        if not st.session_state.user_orders:
            st.info("No orders yet. Start shopping!")
        else:
            for order in st.session_state.user_orders:
                color = "#FFA500" if "Pending" in order['status'] else "#25D366"
                st.markdown(f"""
                <div style="border:1px solid #ddd; padding:15px; border-radius:10px; margin-bottom:10px;">
                    <span style="background:{color};" class="status-badge">{order['status']}</span>
                    <h4>Order #{order['oid']} - {order['item']}</h4>
                    <p>Amount: ₦{order['price']:,} | Date: {order['date']}</p>
                </div>
                """, unsafe_allow_html=True)
                if order['status'] == "Pending Payment":
                    st.write("**Pay to: OPay | 0123456789 | ConfirmAm**")
                    st.link_button("📲 Send Proof to Support", f"https://wa.me/2348000000000?text=Paid%20Order%20{order['oid']}")

    # --- SELL PAGE ---
    elif st.session_state.page == "Sell":
        st.subheader("Merchant Dashboard")
        with st.form("sell_form"):
            b_name = st.text_input("Brand Name")
            p_name = st.text_input("Product Name")
            p_price = st.number_input("Price", min_value=100)
            if st.form_submit_button("Post Live"):
                st.session_state.inventory.append({
                    "id": str(uuid.uuid4())[:4], "name": p_name, "price": p_price, "seller": b_name, "verified": False
                })
                st.success("Live! Note: Verification badge applied after 24h review.")

    # --- LEGAL PAGE (The Flutterwave Requirement) ---
    elif st.session_state.page == "Legal":
        st.subheader("Trust & Safety Policies")
        st.markdown("""
        <div class="policy-box">
            <h4>1. The Escrow Rule</h4>
            <p>ConfirmAm holds buyer payments for 48 hours after delivery. Money is only released to the seller once the buyer confirms "Order Received."</p>
            <h4>2. Refund Policy</h4>
            <p>If the item is not delivered or doesn't match the description, a full refund is processed within 24 hours.</p>
            <h4>3. Support</h4>
            <p>Need help? Contact our 24/7 Escrow Officers via the Tracker tab.</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("---")
        st.button("Contact Support via WhatsApp")

    # Sidebar Logout
    with st.sidebar:
        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.rerun()

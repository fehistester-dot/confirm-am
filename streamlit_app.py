import streamlit as st
import uuid

# 1. High-End Page Configuration
st.set_page_config(page_title="ConfirmAm | Luxury Escrow", page_icon="✨", layout="wide")

# 2. Professional Custom Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #ffffff; }
    .auth-box { max-width: 400px; padding: 40px; border-radius: 20px; background-color: #f8f9fa; margin: auto; border: 1px solid #eee; }
    .product-card { border: 1px solid #f0f0f0; padding: 15px; border-radius: 20px; background-color: #fff; text-align: center; }
    .stButton>button { border-radius: 50px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. Data & Session Initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'orders' not in st.session_state:
    st.session_state.orders = {}

# SETTINGS
ADMIN_WA = "2348012345678" # Your WhatsApp Number

# --- LOGIN GATE ---
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="auth-box">', unsafe_allow_html=True)
        st.title("ConfirmAm")
        st.write("Secure Luxury Fashion Marketplace")
        
        email = st.text_input("Email")
        pwd = st.text_input("Password", type="password")
        
        if st.button("Enter Boutique", use_container_width=True):
            if email and pwd:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Please fill in all fields.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- THE MAIN MARKETPLACE ---
else:
    # Top Premium Greeting Banner
    st.markdown("""
        <div style="background-color:#000; color:#d4af37; padding:20px; border-radius:15px; text-align:center; margin-bottom:25px; border: 1px solid #d4af37;">
            <h2 style="margin:0;">Welcome to the Collection ✨</h2>
            <p style="margin:5px 0 0 0; opacity:0.9;">Verified Buyer: <b>Safe & Secure Escrow Active</b></p>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar for Logout
    with st.sidebar:
        st.title("ConfirmAm")
        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.rerun()

    tab1, tab2, tab3 = st.tabs(["🛍️ Shop", "📤 Sell", "🔒 Payment"])

    with tab1:
        st.header("Latest Arrivals")
        if not st.session_state.inventory:
            st.info("The gallery is currently being updated. Come back soon!")
        else:
            cols = st.columns(2) # 2 items per row for mobile friendly view
            for idx, item in enumerate(st.session_state.inventory):
                with cols[idx % 2]:
                    st.markdown(f'<div class="product-card"><h3>{item["name"]}</h3><h2>₦{item["price"]:,}</h2></div>', unsafe_allow_html=True)
                    if item['image']: st.image(item['image'], use_container_width=True)
                    if st.button(f"Secure Buy", key=f"buy_{idx}"):
                        oid = str(uuid.uuid4())[:6].upper()
                        st.session_state.orders[oid] = {"item": item['name'], "price": item['price']}
                        st.session_state.last_oid = oid
                        st.success(f"Order {oid} Created! Go to Payment Tab.")

    with tab2:
        st.header("Merchant Dashboard")
        with st.form("add_item"):
            name = st.text_input("Product Name")
            price = st.number_input("Price (₦)", min_value=100)
            img = st.file_uploader("Upload Product Photo")
            if st.form_submit_button("Post to Marketplace"):
                st.session_state.inventory.append({"name": name, "price": price, "image": img})
                st.rerun()

    with tab3:
        st.header("Confirm Your Purchase")
        oid_in = st.text_input("Enter Order ID", value=st.session_state.get('last_oid', '')).upper()
        
        if oid_in in st.session_state.orders:
            order = st.session_state.orders[oid_in]
            st.markdown(f"""
            <div style="background-color:#f9f9f9; padding:20px; border-radius:15px; border-left: 5px solid #000;">
                <h4>Paying for: {order['item']}</h4>
                <h3>Amount: ₦{order['price']:,}</h3>
                <p><b>Bank:</b> OPay / Zenith / Kuda<br><b>Name:</b> ConfirmAm Services<br><b>Acct:</b> 0123456789</p>
            </div>
            """, unsafe_allow_html=True)
            
            wa_text = f"Hello! I've paid ₦{order['price']:,} for the {order['item']} (ID: {oid_in})."
            wa_url = f"https://wa.me/{ADMIN_WA}?text={wa_text.replace(' ', '%20')}"
            
            st.write("")
            st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; height:50px; background-color:#25D366; color:white; border:none; border-radius:50px; cursor:pointer; font-weight:bold;">📲 VERIFY VIA WHATSAPP</button></a>', unsafe_allow_html=True)
        else:
            st.info("Your order details will appear here once you select an item.")

import streamlit as st
import uuid

# 1. Premium Page Configuration
st.set_page_config(page_title="ConfirmAm Premium", page_icon="✨", layout="wide")

# 2. "High-End" Custom Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #ffffff; }
    .stHeader { background-color: #000000; padding: 20px; color: white; border-radius: 0 0 20px 20px; }
    .product-card {
        border: 1px solid #f0f0f0;
        padding: 15px;
        border-radius: 20px;
        transition: 0.3s;
        background-color: #fff;
    }
    .product-card:hover { box-shadow: 0px 10px 20px rgba(0,0,0,0.05); transform: translateY(-5px); }
    .price-tag { color: #000; font-weight: 700; font-size: 1.2em; }
    .buy-btn { 
        background-color: #000 !important; 
        color: #fff !important; 
        border-radius: 50px !important; 
        border: none !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Data Initialization
if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'orders' not in st.session_state:
    st.session_state.orders = {}

# YOUR BUSINESS SETTINGS
ADMIN_WA = "2348012345678" # Put your real WhatsApp number here

# --- HEADER SECTION ---
st.markdown('<div class="stHeader"><h1 style="margin:0;">ConfirmAm</h1><p style="opacity:0.8;">The Luxury Standard for Secure Nigerian Fashion</p></div>', unsafe_allow_html=True)
st.write("")

# --- NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["✨ Explore Collection", "📈 Seller Suite", "🔒 Security Vault"])

# --- TAB 1: PREMIUM SHOP ---
with tab1:
    col_s, col_f = st.columns([2, 1])
    with col_s:
        search = st.text_input("🔍 Search for your style...", placeholder="Search for dresses, sets, etc.")
    with col_f:
        category = st.selectbox("Category", ["All Items", "Dresses", "Two-Pieces", "Accessories"])

    st.write("---")
    
    if not st.session_state.inventory:
        st.info("The collection is currently being curated. Check back shortly!")
    else:
        # Displaying products in a clean grid
        cols = st.columns(4) # 4 items per row for a "Pro" look
        for idx, item in enumerate(st.session_state.inventory):
            with cols[idx % 4]:
                st.markdown(f"""
                <div class="product-card">
                    <p style="color:gray; font-size:0.8em; text-transform:uppercase; margin-bottom:5px;">{item.get('cat', 'New Arrival')}</p>
                    <h3 style="margin:0;">{item['name']}</h3>
                    <p class="price-tag">₦{item['price']:,}</p>
                </div>
                """, unsafe_allow_html=True)
                if item['image']: st.image(item['image'], use_container_width=True)
                
                if st.button(f"Secure Purchase", key=f"buy_{idx}", help="Click to buy via ConfirmAm Escrow"):
                    oid = str(uuid.uuid4())[:6].upper()
                    st.session_state.orders[oid] = {"item": item['name'], "price": item['price'], "status": "Pending"}
                    st.session_state.last_oid = oid
                    st.toast(f"Order {oid} created! Proceed to Security Vault.", icon="✅")

# --- TAB 2: SELLER SUITE ---
with tab2:
    st.header("Merchant Dashboard")
    with st.expander("Add New Product to Catalog"):
        name = st.text_input("Product Title")
        price = st.number_input("Market Price (₦)", min_value=100)
        cat = st.selectbox("Product Category", ["Dresses", "Two-Pieces", "Accessories", "Other"])
        img = st.file_uploader("High-Resolution Product Image", type=['jpg', 'png'])
        if st.button("Publish to Marketplace"):
            st.session_state.inventory.append({"name": name, "price": price, "image": img, "cat": cat})
            st.success("Product published successfully.")

# --- TAB 3: SECURITY VAULT ---
with tab3:
    st.header("Secure Payment Verification")
    oid_in = st.text_input("Enter Order Reference", value=st.session_state.get('last_oid', '')).upper()
    
    if oid_in in st.session_state.orders:
        order = st.session_state.orders[oid_in]
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div style="background-color:#f9f9f9; padding:30px; border-radius:20px;">
                <h2 style="margin-top:0;">Payment Summary</h2>
                <p>Item: <b>{order['item']}</b></p>
                <p>Order ID: <b>{oid_in}</b></p>
                <h1 style="color:#000;">₦{order['price']:,}</h1>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.write("### 🏦 Vault Bank Details")
            st.code("Bank: Kuda Bank\nName: ConfirmAm Services\nAcct: 0123456789", language="text")
            
            wa_msg = f"Hello! I've just paid ₦{order['price']:,} for the {order['item']} (ID: {oid_in})."
            wa_url = f"https://wa.me/{ADMIN_WA}?text={wa_msg.replace(' ', '%20')}"
            
            st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; height:50px; background-color:#000; color:white; border:none; border-radius:50px; cursor:pointer; font-weight:bold;">📲 VERIFY PAYMENT VIA WHATSAPP</button></a>', unsafe_allow_html=True)
    else:
        st.write("Enter an active Order Reference to proceed with secure payment.")

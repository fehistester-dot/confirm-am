import streamlit as st
import uuid

# 1. Page Config
st.set_page_config(page_title="ConfirmAm Marketplace", page_icon="🛡️", layout="wide")

# 2. Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .product-card { background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #eee; text-align: center; box-shadow: 0px 4px 10px rgba(0,0,0,0.05); }
    .payment-box { background-color: #f0fff4; padding: 20px; border-radius: 15px; border: 2px solid #28a745; color: #155724; }
    .wa-button { background-color: #25D366 !important; color: white !important; font-weight: bold !important; border-radius: 25px !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Database
if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'orders' not in st.session_state:
    st.session_state.orders = {}

# YOUR WHATSAPP NUMBER (International format without +)
# CHANGE THIS TO YOUR REAL NUMBER SO YOU GET THE MESSAGES
ADMIN_WHATSAPP = "2348012345678" 

st.title("🛡️ ConfirmAm Marketplace")

tab1, tab2, tab3 = st.tabs(["🛒 Browse Shop", "📤 Seller Dashboard", "💳 Payment & Security"])

# --- SHOP ---
with tab1:
    st.header("Latest Marketplace Items")
    if not st.session_state.inventory:
        st.info("Shop is empty. List something!")
    else:
        cols = st.columns(3)
        for idx, item in enumerate(st.session_state.inventory):
            with cols[idx % 3]:
                st.markdown(f'<div class="product-card"><h3>{item["name"]}</h3><h2>₦{item["price"]:,}</h2></div>', unsafe_allow_html=True)
                if item['image']: st.image(item['image'], use_container_width=True)
                
                if st.button(f"Buy Now: {item['name']}", key=f"buy_{idx}"):
                    oid = str(uuid.uuid4())[:6].upper()
                    st.session_state.orders[oid] = {"item": item['name'], "price": item['price'], "status": "Pending"}
                    st.session_state.last_oid = oid
                    st.success(f"Order Created! ID: {oid}")

# --- SELLER ---
with tab2:
    st.header("List a New Product")
    with st.form("add_item"):
        name = st.text_input("Product Name")
        price = st.number_input("Price (₦)", min_value=100)
        img = st.file_uploader("Upload Image", type=['jpg', 'png'])
        if st.form_submit_button("List Now"):
            st.session_state.inventory.append({"name": name, "price": price, "image": img})
            st.rerun()

# --- PAYMENT ---
with tab3:
    st.header("Confirm Your Secure Payment")
    oid_input = st.text_input("Enter Order ID", value=st.session_state.get('last_oid', '')).upper()
    
    if oid_input in st.session_state.orders:
        order = st.session_state.orders[oid_input]
        st.subheader(f"Paying for: {order['item']}")
        
        st.markdown(f"""
        <div class="payment-box">
            <h4>🏦 Transfer exactly ₦{order['price']:,} to:</h4>
            <p><strong>Bank:</strong> OPay / Zenith / Kuda</p>
            <p><strong>Account Name:</strong> ConfirmAm Services</p>
            <p><strong>Account Number:</strong> 0123456789</p>
            <p><i>Reference ID: {oid_input}</i></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("---")
        st.write("### ⚡ Fast-Track Verification")
        st.write("Click below to send your transfer receipt directly to our WhatsApp for instant approval.")
        
        wa_text = f"Hello ConfirmAm! I just paid ₦{order['price']:,} for {order['item']} (Order ID: {oid_input}). Here is my receipt:"
        wa_url = f"https://wa.me/{ADMIN_WHATSAPP}?text={wa_text.replace(' ', '%20')}"
        
        st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; height:50px; background-color:#25D366; color:white; border:none; border-radius:25px; cursor:pointer; font-weight:bold;">📲 Send Receipt via WhatsApp</button></a>', unsafe_allow_html=True)
        
        st.divider()
        st.caption("Once we confirm your receipt on WhatsApp, we will secure the funds and notify the seller to ship.")
    else:
        st.info("Select an item from the shop to start a secure payment.")

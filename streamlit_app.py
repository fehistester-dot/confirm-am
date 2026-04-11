import streamlit as st

# ... (keep your existing page_config and styling) ...

# --- NEW SIDEBAR: THE HARD-WIRED VERSION ---
st.sidebar.image("https://i.postimg.cc/mD3WvH5n/Confirm-Am-Logo-Tick.png", use_container_width=True)
st.sidebar.markdown("<h2 style='text-align:center;'>ConfirmAm</h2>", unsafe_allow_html=True)

st.sidebar.markdown("---")

# 1. THE TRACKING BUTTON (Direct WhatsApp Link)
# This is now the most prominent thing in the sidebar
st.sidebar.subheader("📦 Order Status")
st.sidebar.link_button(
    "Track My Order", 
    "https://wa.me/2347046481507?text=Hello%20ConfirmAm,%20I%20just%20paid%20and%20need%20to%20track%20my%20order", 
    use_container_width=True,
    type="primary" # This makes it a bold blue button
)

st.sidebar.markdown("---")

# 2. THE NAVIGATION
menu = st.sidebar.radio("Go to:", ["🛍️ Shopping Mall", "🛡️ How Escrow Works", "📥 Vendor Portal"])

import streamlit as st
import uuid

# 1. Page & Style Config
st.set_page_config(page_title="ConfirmAm | Member Portal", page_icon="🔒", layout="wide")

st.markdown("""
    <style>
    .auth-box { max-width: 400px; padding: 30px; border-radius: 20px; background-color: #f8f9fa; margin: auto; border: 1px solid #eee; box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
    .stButton>button { border-radius: 50px; font-weight: bold; width: 100%; }
    .toggle-text { text-align: center; margin-top: 15px; cursor: pointer; color: #d4af37; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. State Management
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = "Login" 
if 'inventory' not in st.session_state:
    st.session_state.inventory = []

# --- THE DOORWAY (Sign In / Sign Up) ---
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="auth-box">', unsafe_allow_html=True)
        
        # Switch between Sign In and Sign Up
        if st.session_state.auth_mode == "Login":
            st.markdown("<h2 style='text-align: center;'>Sign In</h2>", unsafe_allow_html=True)
            email = st.text_input("Email", key="li_email")
            pwd = st.text_input("Password", type="password", key="li_pwd")
            if st.button("Enter Boutique"):
                if email and pwd:
                    st.session_state.logged_in = True
                    st.rerun()
            
            if st.button("New here? Create Account", type="secondary"):
                st.session_state.auth_mode = "SignUp"
                st.rerun()

        else:
            st.markdown("<h2 style='text-align: center;'>Sign Up</h2>", unsafe_allow_html=True)
            new_name = st.text_input("Full Name")
            new_email = st.text_input("Email Address")
            new_pwd = st.text_input("Create Password", type="password")
            
            user_role = st.selectbox("I am a:", ["Buyer", "Merchant/Designer"])
            
            if st.button("Join ConfirmAm"):
                if new_email and new_pwd:
                    st.success("Account Created! Now please Sign In.")
                    st.session_state.auth_mode = "Login"
                    st.rerun()
            
            if st.button("Already have an account? Sign In", type="secondary"):
                st.session_state.auth_mode = "Login"
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# --- THE MARKETPLACE (Visible after Login) ---
else:
    # (The Gold Banner and Marketplace code stays exactly the same here)
    st.markdown("""
        <div style="background-color:#000; color:#d4af37; padding:20px; border-radius:15px; text-align:center; margin-bottom:25px; border: 1px solid #d4af37;">
            <h2 style="margin:0;">Welcome to the Collection ✨</h2>
            <p style="margin:5px 0 0 0; opacity:0.9;">Verified Member Access</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.title("ConfirmAm")
        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.rerun()
    
    st.write("### Hello! You are now inside the secure zone.")
    st.info("Start listing your products in the 'Sell' tab or explore the 'Shop'!")

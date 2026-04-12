import streamlit as st

import pandas as pd

import requests

from io import StringIO



# 1. Page Configuration

st.set_page_config(page_title="ConfirmAm Marketplace", page_icon="🛡️", layout="wide")



# 2. THE DATABASE LINKS

SHEET_ID = "1VubDpOo8wOWTOeyhgu-9oMlagyTvRZUqDc6wkXIpfTY"

PRODUCTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

MERCHANTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1626214553"



# 3. THE MASTER KEY FUNCTION

# This function tricks Google into thinking the app is a real person

def get_data(url):

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

    response = requests.get(url, headers=headers)

    return pd.read_csv(StringIO(response.text))



# --- SIDEBAR ---

st.sidebar.title("ConfirmAm 🛡️")

menu = st.sidebar.radio("Navigate", ["🛍️ Shopping Mall", "🏢 Merchant Catalog"])



# --- 1. SHOPPING MALL ---

if menu == "🛍️ Shopping Mall":

    st.header("ConfirmAm Mall")

    try:

        data = get_data(PRODUCTS_URL)

        data.columns = [c.strip().lower() for c in data.columns]

        

        if data.empty:

            st.warning("Sheet is empty!")

        else:

            cols = st.columns(2) # 2 columns is safer for mobile screens

            for i, row in data.iterrows():

                with cols[i % 2]:

                    st.image(row.get('image_url', ''), use_container_width=True)

                    st.write(f"**{row.get('name', 'Product')}**")

                    st.write(f"₦{row.get('price', 0)}")

                    st.link_button("Buy Now", "https://flutterwave.com/pay/ctppxixgdke7")

    except Exception as e:

        st.error(f"Database Error: Please ensure your Google Sheet is Shared to 'Anyone with the link can view'.")



# --- 2. MERCHANT CATALOG ---

elif menu == "🏢 Merchant Catalog":

    st.header("Verified Partners")

    try:

        m_data = get_data(MERCHANTS_URL)

        st.dataframe(m_data, use_container_width=True)

    except:

        st.error("Could not load merchants.")

this is the code I'm using currently

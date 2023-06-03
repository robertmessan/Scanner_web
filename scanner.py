import streamlit as st
import webbrowser
import pyqrcode
from urllib.parse import urlparse
import requests
from PIL import Image

def check_website_security():
    url = url_input.lower()
    parsed_url = urlparse(url)
    if parsed_url.scheme == 'https':
        domain_name = parsed_url.netloc
        if domain_name.startswith("www."):
            domain_name = domain_name[4:]
        domain_name = domain_name.rsplit('.', 1)[0]

        try:
            response = requests.head(url)
            if response.status_code >= 200 and response.status_code <= 299:
                st.success(f"Nom de domaine: {domain_name}")
                qr_button_disabled = False
                connect_button_disabled = False
            else:
                st.error("Le site n'existe pas")
                qr_button_disabled = True
                connect_button_disabled = True
        except requests.exceptions.RequestException:
            st.error("Le site n'existe pas")
            qr_button_disabled = True
            connect_button_disabled = True
    else:
        st.error("Site non sécurisé!")
        qr_button_disabled = True
        connect_button_disabled = True

    return qr_button_disabled, connect_button_disabled

def generate_qrcode():
    url = url_input.lower()
    qr = pyqrcode.create(url)
    qr.png("qrcode.png", scale=6)
    qr_code_image = Image.open("qrcode.png")
    st.image(qr_code_image)

def connect_to_website():
    url = url_input.lower()
    webbrowser.open(url)

st.title("Smart scanner")

url_input = st.text_input("URL du site web")

check_button = st.button("Vérifier", key="check")
if check_button:
    qr_button_disabled, connect_button_disabled = check_website_security()

col1, col2, col3 = st.columns(3)
with col1:
    qr_button_disabled = st.session_state.get("qr_button_disabled", True)
    if qr_button_disabled:
        st.button("Générer QR code", key="generate_qrcode", on_click=None)
    else:
        qr_button_clicked = st.button("Générer QR code", key="generate_qrcode")
        if qr_button_clicked:
            generate_qrcode()

with col2:
    connect_button_disabled = st.session_state.get("connect_button_disabled", True)
    if connect_button_disabled:
        st.button("Se connecter", key="connect", on_click=None)
    else:
        connect_button_clicked = st.button("Se connecter", key="connect")
        if connect_button_clicked:
            connect_to_website()

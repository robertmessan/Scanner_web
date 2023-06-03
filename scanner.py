import streamlit as st
import webbrowser
import pyqrcode
from urllib.parse import urlparse
import requests
from PIL import Image

def check_website_security():
    url = url_input.lower()  # Convertir l'URL en minuscules
    parsed_url = urlparse(url)
    if parsed_url.scheme == 'https':
        domain_name = parsed_url.netloc
        if domain_name.startswith("www."):
            domain_name = domain_name[4:]
        domain_name = domain_name.rsplit('.', 1)[0]  # Supprimer les derniers caractères après le dernier point '.'

        # Vérifier si le site web existe réellement
        try:
            response = requests.head(url)
            if response.status_code >= 200 and response.status_code <= 299:
                st.success(f"Nom de domaine: {domain_name}")
                st.session_state.qr_button_disabled = False
                st.session_state.connect_button_disabled = False
            else:
                st.error("Le site n'existe pas")
                st.session_state.qr_button_disabled = True
                st.session_state.connect_button_disabled = True
        except requests.exceptions.RequestException:
            st.error("Le site n'existe pas")
            st.session_state.qr_button_disabled = True
            st.session_state.connect_button_disabled = True
    else:
        st.error("Site non sécurisé!")
        st.session_state.qr_button_disabled = True
        st.session_state.connect_button_disabled = True

def generate_qrcode():
    url = url_input.lower()  # Convertir l'URL en minuscules
    qr = pyqrcode.create(url)
    qr.png("qrcode.png", scale=6)
    qr_code_image = Image.open("qrcode.png")
    st.image(qr_code_image)

def connect_to_website():
    url = url_input.lower()  # Convertir l'URL en minuscules
    webbrowser.open(url)

st.title("Smart scanner")

# Chargement de l'image du logo

# Zone de texte pour l'URL du site web
url_input = st.text_input("URL du site web")

# Bouton de vérification
check_button = st.button("Vérifier", key="check")
if check_button:
    check_website_security()

# Gestion des boutons
col1, col2, col3 = st.columns(3)
with col1:
    qr_button = st.button("Générer QR code", key="generate_qrcode", disabled=st.session_state.get("qr_button_disabled", True))
    if qr_button:
        generate_qrcode()
with col2:
    connect_button = st.button("Se connecter", key="connect", disabled=st.session_state.get("connect_button_disabled", True))
    if connect_button:
        connect_to_website()
#with col3:
    #st.button("Quitter l'application")


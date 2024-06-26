import streamlit as st
import webbrowser
import pyqrcode
from urllib.parse import urlparse
import requests
from PIL import Image
import time

def check_website_security():
    url = site_url.lower()  
    parsed_url = urlparse(url)
    if parsed_url.scheme == 'https':
        domain_name = parsed_url.netloc
        if domain_name.startswith("www."):
            domain_name = domain_name[4:]
        domain_name = domain_name.rsplit('.', 1)[0]  

        # Vérifier si le site web existe réellement
        try:
            response = requests.head(url)
            if response.status_code >= 200 and response.status_code <= 299:
                st.success(f"Nom de domaine: {domain_name}")
                st.session_state.qr_button_disabled = False
                st.session_state.connect_button_disabled = False
                st.session_state.login_button_disabled = False
                st.session_state.security_criterion_1 = True  
                st.session_state.security_criterion_2 = True  
                
                if response.headers.get('Strict-Transport-Security') is not None:
                    st.session_state.security_criterion_3 = True  
                else:
                    st.session_state.security_criterion_3 = False
                
                # Vérifier si le site est protégé contre les attaques de force brute
                if response.headers.get('X-Frame-Options') == 'SAMEORIGIN':
                    st.session_state.security_criterion_4 = True  
                else:
                    st.session_state.security_criterion_4 = False  
            else:
                st.error("Nous n'avons pas pu analyser ce site. Vérifiez que l'URL saisie correspond exactement au site souhaité!")
                st.session_state.qr_button_disabled = True
                st.session_state.connect_button_disabled = True
                st.session_state.login_button_disabled = True
                st.session_state.security_criterion_1 = False  
                st.session_state.security_criterion_2 = False  
                st.session_state.security_criterion_3 = False  
                st.session_state.security_criterion_4 = False  
        except requests.exceptions.RequestException:
            st.error("Nous n'avons pas réussi à analyser ce site! Soit il a déjà été signalé comme faux site web, soit il est hébergé en tant que site personnel. Veuillez vous assurer que l'orthographe est correcte.")
            st.session_state.qr_button_disabled = True
            st.session_state.connect_button_disabled = True
            st.session_state.login_button_disabled = True
            st.session_state.security_criterion_1 = False  
            st.session_state.security_criterion_2 = False  
            st.session_state.security_criterion_3 = False  
            st.session_state.security_criterion_4 = False  
    else:
        st.error("Site non sécurisé ! Veuillez utiliser 'https' au début de votre URL.")
        st.session_state.qr_button_disabled = True
        st.session_state.connect_button_disabled = True
        st.session_state.login_button_disabled = True
        st.session_state.security_criterion_1 = False  
        st.session_state.security_criterion_2 = False  
        st.session_state.security_criterion_3 = False  
        st.session_state.security_criterion_4 = False  
        
def connect_to_website():
    url1 = site_url.lower()  # Convertir l'URL en minuscules
    webbrowser.open(url1)
    
def generate_qrcode():
    url = site_url.lower()  # Convertir l'URL en minuscules
    qr = pyqrcode.create(url)
    qr.png("qrcode.png", scale=6)
    qr_code_image = Image.open("qrcode.png")
    st.image(qr_code_image)


def login_to_website():
    url2 = site_url.lower()  # Convertir l'URL en minuscules
    webbrowser.open(url2)

def reset_application():
    st.session_state.qr_button_disabled = True
    st.session_state.connect_button_disabled = True
    st.session_state.login_button_disabled = True
    st.session_state.security_criterion_1 = False
    st.session_state.security_criterion_2 = False
    st.session_state.security_criterion_3 = False
    st.session_state.security_criterion_4 = False
    st.session_state.site_url = ""

#----------------------------
st.markdown('<h1 style="color: green;">Smart scanner</h1>', unsafe_allow_html=True)
st.markdown('<h2 style="color: purple;">Important🔴</h2>', unsafe_allow_html=True)
phrasew = """Cette application est un prototype d'une application mobile en cours de développement.**Elle peut ne pas analyser certains sites**.Veuillez ne considérer que des sites déclarés sécurisés avec tous les critères.Veuillez noter également que ces critères ne vous rendent pas totalement invulnérable.**Le risque 0 n'existe pas!** Si vous avez des propositions, **n'hésitez pas à me contacter.** 
"""
st.subheader(phrasew)
 
# Zone de texte pour l'URL du site web
site_url = st.text_input("URL du site web", value=st.session_state.get("site_url", ""))

# Bouton de vérification
check_button = st.button("Vérifier", key="check")
if check_button:
    check_website_security()

# Gestion des boutons
col1, col2, = st.columns(2)
with col1:
    qr_button = st.button("Générer QR code", key="generate_qrcode", disabled=st.session_state.get("qr_button_disabled", True))
    if qr_button:
        generate_qrcode()
with col2:
    reset_button = st.button("Réinitialiser", key="reset")
if reset_button:
    reset_application()



# Autres critères de sécurité
if st.session_state.get("security_criterion_1", False):
    st.success("Critère de sécurité 1 : Site existant")
else:
    st.error("Critère de sécurité 1 : Site non existant")

if st.session_state.get("security_criterion_2", False):
    st.success("Critère de sécurité 2 : Site sécurisé")
else:
    st.error("Critère de sécurité 2 : Site non sécurisé (Pensez à 'HTTPS')")

if st.session_state.get("security_criterion_3", False):
    st.success("Critère de sécurité 3 : Certificat SSL valide")
else:
    st.error("Critère de sécurité 3 : Certificat SSL non valide")

if st.session_state.get("security_criterion_2", False):
    st.success("Critère de sécurité 4 : Données non interceptables")
else:
    st.error("Critère de sécurité 4 : Données interceptables")

st.markdown("Réalisé avec💖par Robert ")    
    
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


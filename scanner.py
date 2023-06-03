import tkinter as tk
import webbrowser
import pyqrcode
from urllib.parse import urlparse
from PIL import ImageTk, Image
import requests

def check_website_security():
    url = url_entry.get().lower()  # Convertir l'URL en minuscules
    parsed_url = urlparse(url)
    
    if parsed_url.scheme == 'https':
        domain_name = parsed_url.netloc
        if domain_name.startswith("www."):
            domain_name = domain_name[4:]
        domain_name = domain_name.rsplit('.', 1)[0]  # Supprimer les derniers caractères après le dernier point '.'
        
        # Vérifier si le site web existe réellement
        try:
            response = requests.head(url)
            if response.status_code >= 200 or response.status_code <= 299:
                result_label.config(text=f"Nom de domaine: {domain_name}", fg='green')
                generate_qrcode_button.config(state='normal')
                connect_button.config(state='normal')
            else:
                result_label.config(text="Le site n'existe pas", fg='red')
                generate_qrcode_button.config(state='disabled')
                connect_button.config(state='disabled')
        except requests.exceptions.RequestException:
            result_label.config(text="Le site n'existe pas", fg='red')
            generate_qrcode_button.config(state='disabled')
            connect_button.config(state='disabled')
    else:
        result_label.config(text="Site non sécurisé", fg='red')
        generate_qrcode_button.config(state='disabled')
        connect_button.config(state='disabled')
    qr_code_label.config(image="")

def generate_qrcode():
    url = url_entry.get().lower()  # Convertir l'URL en minuscules
    qr = pyqrcode.create(url)
    qr.png("qrcode.png", scale=6)
    qr_code_image = ImageTk.PhotoImage(Image.open("qrcode.png"))
    qr_code_label.config(image=qr_code_image)
    qr_code_label.image = qr_code_image

def connect_to_website():
    url = url_entry.get().lower()  # Convertir l'URL en minuscules
    webbrowser.open(url)

def close_app():
    root.destroy()

root = tk.Tk()
root.title("Smart scanner")

# Chargement de l'image du logo
logo_image = Image.open("Mon_logo.png").resize((150, 150))
logo_photo = ImageTk.PhotoImage(logo_image)

# Étiquette pour afficher le logo au niveau du titre
logo_label = tk.Label(root, image=logo_photo)
logo_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

# Zone de texte pour l'URL du site web
url_label = tk.Label(root, text="URL du site web:", font=("Arial", 14, "bold"))
url_label.grid(row=1, column=0, sticky="W")

url_entry = tk.Entry(root, width=30, font=("Arial", 12))
url_entry.grid(row=1, column=1, padx=10, pady=10)

# Bouton de vérification
check_button = tk.Button(root, text="Vérifier", command=check_website_security, bg='blue', fg='white', font=("Arial", 12, "bold"))
check_button.grid(row=1, column=2, padx=10, pady=10)

# Étiquette de résultat
result_label = tk.Label(root, text="", font=("Arial", 14, "bold"))
result_label.grid(row=2, columnspan=3, padx=10, pady=10)

# Étiquette pour afficher le QR code
qr_code_label = tk.Label(root)
qr_code_label.grid(row=3, columnspan=3, padx=10, pady=10)

# Bouton de génération de QR code
generate_qrcode_button = tk.Button(root, text="Générer QR code", command=generate_qrcode, state='disabled', bg='orange', fg='black', font=("Arial", 12, "bold"))
generate_qrcode_button.grid(row=4, column=0, padx=10, pady=10)

# Bouton de connexion
connect_button = tk.Button(root, text="Se connecter", command=connect_to_website, state='disabled', bg='purple', fg='white', font=("Arial", 12, "bold"))
connect_button.grid(row=4, column=1, padx=10, pady=10)

# Bouton de fermeture
close_button = tk.Button(root, text="Fermer", command=close_app, bg='red', fg='white', font=("Arial", 12, "bold"))
close_button.grid(row=4, column=2, padx=10, pady=10)

root.mainloop()

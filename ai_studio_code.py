import streamlit as st
import pdf2image
import easyocr
import re
import os

# Configuration de l'OCR
reader = easyocr.Reader(['en', 'fr'])

st.title("Aero-Rename Tool")
st.write("Glissez vos scans PDF ici pour les renommer automatiquement.")

uploaded_files = st.file_uploader("Choisir les PDF", accept_multiple_files=True, type="pdf")

if uploaded_files:
    for uploaded_file in uploaded_files:
        # 1. Convertir PDF en Image (Page 4 pour la clarté)
        images = pdf2image.convert_from_bytes(uploaded_file.read(), first_page=4, last_page=4)
        
        # 2. OCR
        import numpy as np
        img_array = np.array(images[0])
        results = reader.readtext(img_array, detail=0)
        full_text = " ".join(results)
        
        # 3. Extraction WO et WP
        wo = re.search(r'WO-?\s*(\d{6})', full_text)
        wp = re.search(r'WP-?\s*(\d{4})', full_text)
        
        if wo and wp:
            new_name = f"{wo.group(1)}_{wp.group(1)}.pdf"
            st.success(f"Fichier identifié : {new_name}")
            # Ici on proposerait le téléchargement du fichier renommé
        else:
            st.error(f"Impossible de lire les numéros sur {uploaded_file.name}")
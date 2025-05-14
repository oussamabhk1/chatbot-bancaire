import streamlit as st
import os
import tempfile
from utils.working_llama_detection import extract_from_image
import json

# Titre et description
st.set_page_config(page_title="Chatbot Bancaire Multilingue", page_icon="🤖")
st.title("📄 Analyse d'image bancaire")
st.markdown("Uploader une image (facture, relevé bancaire, etc.) et je vais en extraire les informations.")

# Upload d'image
uploaded_file = st.file_uploader("Uploader une image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Créer un répertoire temporaire
    with tempfile.TemporaryDirectory() as tmpdir:
        # Chemin complet vers l'image uploadée
        image_path = os.path.join(tmpdir, uploaded_file.name)
        
        # Sauvegarder l'image dans le répertoire temporaire
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Dossier de sortie pour le JSON
        output_dir = os.path.join(tmpdir, "extracted_info_json")

        # Extraction des données
        json_file_path = extract_from_image(image_path, output_dir)

        # Charger les données extraites
        with open(json_file_path, "r", encoding="utf-8") as json_file:
            extracted_data = json.load(json_file)

        # Affichage des résultats
        st.success("✅ Données extraites avec succès !")
        st.json(extracted_data)

import streamlit as st
import os
import tempfile
from utils.working_llama_detection import extract_from_image
from utils.text_processing import get_answer_from_question, load_faq_data

# Titre et description
st.set_page_config(page_title="Chatbot Bancaire Multilingue", page_icon="🤖")
st.title("🤖 Chatbot Bancaire Multilingue")
st.markdown("Posez vos questions liées à la banque (en 🇫🇷, 🇬🇧 ou 🇸🇦), ou envoyez une image.")

# Chargement des données FAQ
faq_data = load_faq_data("cleanedTranslatedBankFAQs.csv")

# Interface utilisateur
uploaded_file = st.file_uploader("Uploader une image (JPG/PNG)", type=["jpg", "png", "jpeg"])
user_input = st.text_area("Ou posez votre question ici...")

if st.button("Envoyer"):
    if uploaded_file is not None:
        # Gestion de l'image
        with tempfile.TemporaryDirectory() as tmpdir:
            image_path = os.path.join(tmpdir, uploaded_file.name)
            
            # Sauvegarder l'image uploadée
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            output_dir = os.path.join(tmpdir, "extracted_info_json")
            
            # Extraire les données
            extract_from_image(image_path, output_dir)

            json_result_path = os.path.join(output_dir, uploaded_file.name.replace(".jpg", ".json").replace(".png", ".json"))

            with open(json_result_path, "r", encoding="utf-8") as f:
                extracted_data = json.load(f)

            st.subheader("📄 Données extraites :")
            st.json(extracted_data)

    elif user_input.strip() != "":
        # Gestion du texte
        answer = get_answer_from_question(user_input, faq_data)
        st.success(f"**💬 Réponse :** {answer}")
    else:
        st.warning("Veuillez entrer une question ou télécharger une image.")

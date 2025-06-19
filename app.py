
import streamlit as st
import openai
from fpdf import FPDF
import leafmap.foliumap as leafmap

st.set_page_config(page_title="GeoTrace Afrique", layout="wide")
st.title("🌍 GeoTrace Afrique – Données Environnementales & Rapports IA")

# Carte interactive
st.subheader("🗺️ Visualisation SIG")
m = leafmap.Map(center=[-4.8, 11.8], zoom=8)
m.add_basemap("SATELLITE")
m.to_streamlit(height=500)

# Rapport IA
st.subheader("📄 Générateur de Rapport IA")
openai.api_key = st.secrets["openai_api_key"]

def analyse_environnement(zone, ndvi, pollution):
    prompt = f"""
    Génère un résumé d'analyse environnementale pour la zone {zone} :
    - Indice de végétation NDVI : {ndvi}
    - Niveau de pollution : {pollution}
    Propose des recommandations ou risques environnementaux à surveiller.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def generer_pdf(zone, ndvi, pollution, analyse):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="GeoTrace Afrique – Rapport Environnemental", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Zone analysée : {zone}", ln=True)
    pdf.cell(200, 10, txt=f"NDVI : {ndvi}", ln=True)
    pdf.cell(200, 10, txt=f"Pollution : {pollution}", ln=True)
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=f"Analyse IA :\n{analyse}")
    pdf.output("rapport.pdf")
    return "rapport.pdf"

zone = st.text_input("Nom de la zone analysée", "Pointe-Noire")
ndvi = st.slider("Valeur NDVI", 0.0, 1.0, 0.45)
pollution = st.selectbox("Niveau de pollution", ["Faible", "Modérée", "Élevée"])

if st.button("Générer le rapport PDF"):
    with st.spinner("Analyse IA en cours..."):
        analyse = analyse_environnement(zone, ndvi, pollution)
        chemin_pdf = generer_pdf(zone, ndvi, pollution, analyse)
        with open(chemin_pdf, "rb") as file:
            st.download_button(
                label="📄 Télécharger le rapport PDF",
                data=file,
                file_name="rapport_environment.pdf",
                mime="application/pdf"
            )

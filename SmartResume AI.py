import streamlit as st
import google.generativeai as genai
import pypdf as pdf

genai.configure(api_key="AIzaSyB4wdCGmCppGyByY5P4oOKEul-XWB8EpiU")

def get_ai_response(text, job_description):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    En tant qu'assistant RH IA, analyse le CV suivant par rapport à l'offre d'emploi.
    
    CV: {text}
    Offre d'emploi: {job_description}
    
    Fournis une réponse structurée en français :
    1. Taux de correspondance (0-100%)
    2. Mots-clés manquants importants
    3. Recommandations concrètes d'amélioration
    """
    response = model.generate_content(prompt)
    return response.text

st.set_page_config(page_title="SmartResume AI", page_icon="🤖", layout="wide")
st.title("🤖 SmartResume AI")
st.subheader("Analyse et optimisation de CV par l'Intelligence Artificielle")

col1, col2 = st.columns(2)

with col1:
    job_desc = st.text_area("1. Collez l'offre d'emploi (Job Description) :", height=250)
    uploaded_file = st.file_uploader("2. Chargez le CV (Format PDF) :", type=["pdf"])

with col2:
    st.write("3. Rapport d'analyse de l'IA :")
    if st.button("Lancer l'analyse du projet", use_container_width=True):
        if uploaded_file and job_desc:
            with st.spinner("Analyse du CV en cours par l'IA..."):
                reader = pdf.PdfReader(uploaded_file)
                resume_text = "".join([page.extract_text() for page in reader.pages])
                
                analysis = get_ai_response(resume_text, job_desc)
                st.success("Analyse terminée avec succès !")
                st.markdown(analysis)
        else:
            st.error("Veuillez remplir l'offre d'emploi et charger un fichier PDF.")

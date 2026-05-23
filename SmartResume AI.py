import streamlit as st
import pypdf as pdf
import requests
import json

def get_ai_response(text, job_description, api_key):
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    if not text.strip():
        text = "[Le texte du CV n'a pas pu être extrait]"

    prompt = f"""
    En tant qu'expert en recrutement et conseiller de carrière professionnel, analyse de manière critique le CV fourni par rapport à l'offre d'emploi (Job Description) suivante.
    
    Offre d'emploi :
    {job_description}
    
    CV du candidat :
    {text}
    
    Génère un rapport d'évaluation complet, constructif et rigoureux, rédigé exclusivement en français, en suivant exactement cette structure Markdown :

    ### 📊 Rapport d'évaluation générale
    **Taux de correspondance global :** [Indique un pourcentage estimé entre 0% et 100% basé sur la pertinence des compétences]
    
    ---

    ### 🛠️ Analyse des compétences clés
    * **Points forts du profil :** [Énumère 2 ou 3 compétences clés du candidat qui correspondent parfaitement à l'offre]
    * **Mots-clés et technologies manquants :** [Identifie les technologies, concepts clés ou outils indispensables de l'offre qui ne figurent pas dans le CV]

    ---

    ### 💡 Recommandations stratégiques d'optimisation
    1.  **Amélioration du contenu :** [Donne un conseil précis sur la façon de reformuler ou de valoriser une expérience ou un projet universitaire en MIASHS pour mieux coller à l'offre]
    2.  **Mise en valeur technique :** [Conseille l'ajout de projets concrets, par exemple en mentionnant le développement de cette application d'IA (SmartResume AI) développée à l'Université Paris Nanterre]
    """
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            try:
                err_data = response.json()
                return f"❌ Erreur API Google ({response.status_code}) : {err_data['error']['message']}"
            except:
                return f"❌ Erreur Serveur Google (Code {response.status_code}). Vérifiez les restrictions de votre clé API."
                
        response_data = response.json()
        
      
        return response_data['candidates'][0]['content']['parts'][0]['text']
        
    except Exception as e:
        return f"❌ Erreur de connexion : {str(e)}"


st.set_page_config(page_title="SmartResume AI", page_icon="🤖", layout="wide")
st.title("🤖 SmartResume AI")
st.subheader("Analyse et optimisation de CV par l'Intelligence Artificielle")


with st.sidebar:
    st.header("🔑 Configuration")
    user_api_key = st.text_input("Entrez votre clé API Gemini :", type="password", help="Obtenez une clé gratuite sur Google AI Studio")
    st.markdown("---")
    st.caption("Projet informatique - Université Paris Nanterre")
    st.caption("Développé par : ZUIEV Volodymyr")


col1, col2 = st.columns(2)

with col1:
    job_desc = st.text_area("1. Collez l'offre d'emploi (Job Description) :", height=200)
    uploaded_file = st.file_uploader("2. Chargez le CV (Format PDF) :", type=["pdf"])

with col2:
    st.write("3. Rapport d'analyse de l'IA :")
    if st.button("Lancer l'analyse du projet", use_container_width=True):
        if not user_api_key:
            st.error("Veuillez entrer votre clé API Gemini dans la barre latérale gauche 🔑")
        elif uploaded_file and job_desc:
            with st.spinner("Analyse du CV en cours par l'IA..."):
                try:
                    reader = pdf.PdfReader(uploaded_file)
                    resume_text = ""
                    for page in reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            resume_text += page_text + "\n"
                except Exception as pdf_err:
                    st.error(f"Erreur de lecture PDF : {pdf_err}")
                    resume_text = ""
                
                analysis = get_ai_response(resume_text, job_desc, user_api_key)
                
                if "❌" in analysis:
                    st.error(analysis)
                else:
                    st.success("Analyse terminée avec succès !")
                    st.markdown(analysis)
        else:
            st.error("Veuillez remplir l'offre d'emploi et charger un fichier PDF.")

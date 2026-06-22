import streamlit as st

""" Page d'accueil de l'application Streamlit pour l'analyse concurrentielle des applications mobiles.
Cette page sert d'introduction et de contexte pour l'ensemble de l'application. Elle présente les objectifs du projet,
la méthodologie adoptée, et les différentes étapes du pipeline analytique qui seront explorées dans les pages suivantes.
L'objectif est de fournir une vue d'ensemble claire et engageante pour orienter l'utilisateur dans son parcours à travers
les modules d'extraction, de visualisation et d'analyse de sentiment. Fonctionnalités principales : 
Présentation du projet, Contexte et objectifs, Méthodologie et pipeline analytique, Aperçu des modules applicatifs, Stack technique utilisée, Cadre académique et auteurs. 
"""

# Configuration de la page en mode Large
st.set_page_config(
    page_title="Market Insights Dashboard", 
    page_icon="📈", 
    layout="wide"
)


# EN-TÊTE ET TITRE STRATÉGIQUE

st.title("📈Plateforme d'Audit Concurrentiel & Business Intelligence")
st.subheader("Analyse Prédictive et Sémantique du Marché des Applications Mobiles")
st.markdown("---")


# BANNER : CONTEXTE DU PROJET (Cadre Pro)

with st.container(border=True):
    st.markdown("""
    ### 📊 Résumé Exécutif
    Cette application analytique a été conçue pour transformer des données brutes issues du **Google Play Store** en insights stratégiques exploitables. 
    Grâce à une architecture multi-pages optimisée, elle combine le **Data Scraping** en temps réel, la **Business Intelligence (BI)** interactive, 
    et le **Traitement Automatique du Langage Naturel (NLP)** par Intelligence Artificielle pour auditer l'écosystème concurrentiel d'un secteur cible.
    """)

st.write("") # Espace de respiration visuelle


# SECTION ARCHITECTURE : LES 3 PIELIERS EN CARTES

st.markdown("### 🗺️ Cartographie des Modules Applicatifs")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown("#### 🔍 1. Extraction Brute")
        st.markdown("""
        **Module :** `Results Tables`
        * **Technologie :** API Scraper
        * **Rôle :** Collecte de masse en temps réel selon les mots-clés du marché.
        * **Données :** Identification des scores, prix, catégories et développeurs actifs.
        """)

with col2:
    with st.container(border=True):
        st.markdown("#### 📊 2. Macro-Visualisation")
        st.markdown("""
        **Module :** `Visualizations`
        * **Technologie :** Plotly Express (BI)
        * **Rôle :** Analyse de la structure et de la dispersion du marché.
        * **Données :** Box Plots de variance, Donut charts de parts de marché et matrices de prix.
        """)

with col3:
    with st.container(border=True):
        st.markdown("#### 🧠 3. Micro-Sémantique")
        st.markdown("""
        **Module :** `Sentiment Analysis`
        * **Technologie :** Deep Learning (DistilBERT)
        * **Rôle :** Analyse de la polarité et de la charge émotionnelle des avis clients.
        * **Données :** Registre d'audit sémantique et KPIs de réputation de marque.
        """)

st.markdown("---")

# 
# PIED DE PAGE : STACK TECHNIQUE & CADRE ACADÉMIQUE
# 
col_tech, col_auth = st.columns([6, 4])

with col_tech:
    st.markdown("#### Stack Technique Industrielle")
    st.markdown("""
    * **Interface & Déploiement :** Streamlit (v1.58.0) & Streamlit Cloud
    * **Moteur d'Ingénierie IA :** Hugging Face Transformers & PyTorch (Inférence NLP)
    * **Moteur Graphique BI :** Plotly Express Interactive Engine
    * **Traitement de Données :** Pandas & NumPy Vectorization
    """)

with col_auth:
    st.markdown("#### Cadre Académique")
    with st.container(border=True):
        st.markdown("""
        * **Établissement :** École Nationale Supérieure d'Informatique et d'Analyse des Systèmes (**ENSIAS**)
        * **Spécialisation :** Business Intelligence & Analytics (**BI&A**)
        * **Projet :** Lab Évalué d'Introduction à la Data Science
        * **Auteurs :** *[Ajoute ton nom et celui de ton binôme ici]*
        """)
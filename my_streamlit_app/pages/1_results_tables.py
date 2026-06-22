import streamlit as st
import pandas as pd
from utils import get_search_results  # Importation de notre moteur de scraping de utils.py

""" Page de résultats de l'application Streamlit pour l'analyse concurrentielle des applications mobiles.
Cette page permet à l'utilisateur de saisir un mot-clé, d'extraire les applications correspondantes du Google Play Store
et d'afficher les résultats dans un tableau interactif. Le tableau fournit des informations clés sur chaque application, 
telles que le nom, le développeur, la note, le nombre d'installations, le prix et la catégorie. Les données extraites sont 
stockées dans le Session State de Streamlit pour être utilisées dans les pages suivantes de l'application, notamment pour 
la visualisation et l'analyse de sentiment. Fonctionnalités principales :  Extraction des applications du Google Play Store,
Affichage des résultats dans un tableau interactif, Stockage des données dans le Session State"""


# 1. CONFIGURATION ET INTERFACE DE LA PAGE

st.set_page_config(page_title="Tableau des Résultats", page_icon="🔍", layout="wide")

st.title("🔍 Extraction & Analyse Comparative des Concurrents")
st.markdown("""
Cette page permet de cartographier l'écosystème des applications mobiles selon votre mot-clé.
Les données collectées serviront de base pour les modules de visualisation et d'analyse de sentiment.
""")


# 2. ZONE DE RECHERCHE (INPUT WIDGETS)
# Utilisation d'un conteneur pour regrouper visuellement les commandes de recherche

with st.container(border=True):
    col_input, col_button = st.columns([4, 1])
    
    with col_input:
        # Widget d'entrée de texte avec une valeur par défaut pertinente pour le Lab
        query = st.text_input(
            "Entrez un mot-clé de recherche (ex: AI mental health wellness, Note taking app) :",
            value="AI mental health wellness"
        )
    
    with col_button:
        # Espacement vertical pour aligner le bouton avec le champ de texte
        st.write("")
        st.write("")
        bouton_recherche = st.button("Lancer l'extraction", use_container_width=True)


# 3. GESTION DU SCRAPING ET DU SESSION STATE (PERSISTANCE DES DONNÉES)
# Si l'utilisateur clique sur le bouton, on lance le scraping et on stocke dans le Session State

if bouton_recherche and query:
    with st.spinner(f"Scraping des applications pour '{query}' en cours... Veuillez patienter..."):
        try:
            # Appel de la fonction de scraping (récupère les 30 meilleures apps pour avoir un échantillon solide)
            df_results = get_search_results(query, count=30)
            
            if not df_results.empty:
                # SAUVEGARDE CRUCIALE : On stocke les données et la requête dans la mémoire globale de Streamlit
                st.session_state['search_results'] = df_results
                st.session_state['current_query'] = query
                st.success(f"Extraction réussie ! {len(df_results)} applications trouvées.")
            else:
                st.warning("Aucun résultat trouvé pour ce mot-clé.")
        except Exception as e:
            st.error(f"Erreur technique lors du scraping : {e}")


# 4. AFFICHAGE ET INTERPRÉTATION ANALYTIQUE
# Si des données existent déjà dans la session (soit venant d'être scrapées, soit d'une page précédente)

if 'search_results' in st.session_state:
    df_a_afficher = st.session_state['search_results']
    req_actuelle = st.session_state['current_query']
    
    st.subheader(f"📊 Benchmarking des données pour : '{req_actuelle}'")
    
    # Métriques clés pour donner un aspect BI (Business Intelligence) immédiat
    m1, m2, m3 = st.columns(3)
    m1.metric("Applications Analysées", len(df_a_afficher))
    m2.metric("Note Moyenne du Marché", f"{df_a_afficher['score'].mean():.2f} / 5")
    # Calcul rapide du nombre d'applications payantes
    nb_payantes = len(df_a_afficher[df_a_afficher['price'] > 0])
    m3.metric("Applications Payantes", f"{nb_payantes} ({(nb_payantes/len(df_a_afficher))*100:.1f}%)")
    
    st.write("")
    
    # Affichage du tableau interactif avec configuration optimisée des colonnes
    st.dataframe(
        df_a_afficher,
        use_container_width=True,
        column_config={
            "appId": st.column_config.TextColumn("ID Application"),
            "title": st.column_config.TextColumn("Nom de l'App"),
            "developer": st.column_config.TextColumn("Développeur"),
            "score": st.column_config.NumberColumn("Note Étoiles", format="%.2f "),
            "installs": st.column_config.TextColumn("Téléchargements"),
            "price": st.column_config.NumberColumn("Prix", format="$%.2f"),
            "genre": st.column_config.TextColumn("Catégorie")
        }
    )
    
    # Section d'interprétation demandée par le livrable du Lab
    st.write("")
    with st.expander("Note d'Analyse Concurrentielle (Interprétation des données)", expanded=True):
        st.markdown(f"""
        **Observations préliminaires sur le mot-clé *"{req_actuelle}"* :**
        * Le marché présente une note moyenne globale de **{df_a_afficher['score'].mean():.2f} **, ce qui indique un niveau d'exigence utilisateur élevé.
        * La majorité des solutions adoptent un modèle économique de type **{"Gratuit / Freemium" if nb_payantes == 0 else "Mixte (Gratuit & Payant)"}**.
        * *Rendez-vous sur la page des Visualisations pour explorer les graphiques avancés de cette distribution.*
        """)
else:
    # Message d'accueil si aucune recherche n'a encore été effectuée
    st.info("Le tableau de bord est vide. Saisissez un mot-clé ci-dessus et cliquez sur 'Lancer l'extraction' pour générer les données.")
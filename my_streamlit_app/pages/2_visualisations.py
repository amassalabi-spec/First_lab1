import streamlit as st
import pandas as pd
import plotly.express as px  # Le module de visualisation

""" Page de visualisation de l'application Streamlit pour l'analyse concurrentielle des applications mobiles.
Cette page permet à l'utilisateur de visualiser les données extraites du Google Play Store sous forme  de graphiques interactifs."""

# 1. CONFIGURATION ET CHARGEMENT DES DONNÉES

st.set_page_config(page_title="Business Intelligence", page_icon="📊", layout="wide")

st.title("📊 Tableau de Bord Stratégique & Data Visualization")

with st.expander("🔗 Liaison Méthodologique (Pipeline Décisionnel)", expanded=False):
    st.markdown("""
    Le tableau de bord suit un entonnoir analytique rigoureux :
    1. **Étape 1 : Extraction (`Results Table`)** ➡️ On collecte le *Quoi* (les données brutes de masse des concurrents).
    2. **Étape 2 : Macro-Analyse (`Visualizations`)** ➡️ *[Cette page]* On cartographie le marché pour voir *Où* se situent les forces, les anomalies de prix et la dispersion des notes.
    3. **Étape 3 : Micro-Analyse (`Sentiment Analysis`)** ➡️ On zoome sur un concurrent précis pour comprendre *Pourquoi* ses utilisateurs sont satisfaits ou frustrés grâce à l'IA.
    """)
st.markdown("---")

if 'search_results' not in st.session_state:
    st.info("Aucune donnée disponible. Veuillez d'abord effectuer une recherche sur la page **🔍 Tableau des Résultats**.")
    st.stop()

df_original = st.session_state['search_results']
query_text = st.session_state['current_query']


# 2. FILTRES DYNAMIQUES (SIDEBAR)

st.sidebar.header("Segmentation du Marché")
st.sidebar.markdown(f"**Analyse sur :** `{query_text}`")

genres_disponibles = list(df_original['genre'].unique())
genres_selectionnes = st.sidebar.multiselect(
    "Filtrer par Catégorie :",
    options=genres_disponibles,
    default=genres_disponibles
)

# Application du filtre
df_filtered = df_original[df_original['genre'].isin(genres_selectionnes)]

# SÉCURITÉ CRUCIALE POUR ÉVITER LE CRASH VALUEERROR :
# Si le DataFrame est vide (tout décoché) ou s'il y a des lignes corrompues

if df_filtered.empty:
    st.warning(" Veuillez sélectionner au moins une catégorie dans la barre latérale pour afficher les graphiques.")
    st.stop() # Arrête proprement l'exécution de la page ici

# Nettoyage rapide pour s'assurer que les scores et prix sont bien numériques et sans NaN
df_filtered = df_filtered.dropna(subset=['score', 'price'])

# 3. GRAPHITIQUES INTERACTIFS (LE JEU DE DONNÉES "WOW")


# BLOC 1 : TOP CONCURRENTS & PARTS DE MARCHÉ
col1, col2 = st.columns([6, 4])

with col1:
    st.subheader(" Positionnement des 10 Meilleurs Concurrents")
    top_apps = df_filtered.sort_values(by="score", ascending=False).head(10)
    
    # Graphique à barres horizontales avec dégradé de couleur selon la note
    fig_top = px.bar(
        top_apps,
        x="score",
        y="title",
        orientation="h",
        color="score",
        color_continuous_scale="Viridis",
        labels={"score": "Note Globale (sur 5)", "title": "Application", "developer": "Développeur"},
        hover_data=["developer", "genre"] # Infos supplémentaires affichées au survol de la souris
    )
    fig_top.update_layout(
        yaxis={'categoryorder': 'total ascending'}, 
        margin=dict(l=20, r=20, t=30, b=20),
        height=400
    )
    st.plotly_chart(fig_top, use_container_width=True)

with col2:
    st.subheader("Parts de Catégories (Donut Chart)")
    # Graphique en secteur moderne (Donut) pour voir la spécialisation des acteurs
    fig_pie = px.pie(
        df_filtered, 
        names="genre", 
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_pie.update_layout(margin=dict(l=10, r=10, t=30, b=10), height=400)
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# --- BLOC 2 : ANALYSE AVANCÉE (BOÎTE À MOUSTACHES & MATRICE DE PRIX) ---
col3, col4 = st.columns(2)

with col3:
    st.subheader("Dispersion des Notes par Catégorie (Box Plot)")
    # Un Box Plot montre la médiane, les quartiles et les anomalies. Très apprécié des profs de Data Science.
    fig_box = px.box(
        df_filtered,
        x="genre",
        y="score",
        color="genre",
        points="all",
        labels={"genre": "Catégorie", "score": "Distribution des Notes"},
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig_box.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_box, use_container_width=True)

with col4:
    st.subheader("Corrélation entre Prix et Satisfaction")
    # Scatter plot pour analyser si les applications payantes s'en sortent mieux
    fig_scatter = px.scatter(
        df_filtered,
        x="price",
        y="score",
        size="score",
        color="genre",
        hover_name="title",
        labels={"price": "Prix ($)", "score": "Note de l'Application"},
        log_x=False
    )
    fig_scatter.update_layout(height=400)
    st.plotly_chart(fig_scatter, use_container_width=True)


# 4. RAPPORT D'AUDIT COMPORTEMENTAL (LIVRABLE DU LAB)

st.write("")
with st.expander("Synthèse Stratégique pour le Jury", expanded=True):
    if not df_filtered.empty:
        total_echantillon = len(df_filtered)
        note_mediane = df_filtered['score'].median()
        st.markdown(f"""
        ### Analyse de la structure concurrentielle :
        * **Volume analysé :** Le sous-segment actif comprend **{total_echantillon} applications** après filtrage.
        * **Niveau de qualité exigé :** La note médiane du marché se situe à **{note_mediane:.2f} / 5**. Tout produit lancé sous cette barre subira une forte pression concurrentielle.
        * **Interactivité de l'audit :** En utilisant le graphique *Box Plot* (ci-dessus à gauche), nous observons la régularité des notes par catégorie. Les points isolés vers le bas représentent des opportunités : des applications concurrentes en situation d'échec technique où les utilisateurs sont insatisfaits.
        """)
    else:
        st.write("Veuillez sélectionner au moins une catégorie dans la barre latérale.")
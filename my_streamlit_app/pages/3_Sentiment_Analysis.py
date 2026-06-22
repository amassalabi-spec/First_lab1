import streamlit as st
import pandas as pd
import plotly.express as px  # Le moteur de rendu haut de gamme
from utils import analyser_sentiments_application  # Importation de notre nouveau moteur IA

""" Page d'analyse de sentiment de l'application Streamlit pour l'analyse concurrentielle des applications mobiles.
Cette page permet à l'utilisateur de sélectionner une application concurrente, d'extraire les commentaires des utilisateurs et 
d'analyser leur sentiment à l'aide d'un modèle de Deep Learning pré-entraîné.Le tableau de bord fournit des métriques clés sur 
la répartition des sentiments, un graphique interactif et un registre d'audit des commentaires, offrant ainsi une vue complète 
de la perception des utilisateurs. Le module d'interprétation cognitive fournit des insights stratégiques pour aider à la prise
de décision et à l'amélioration de la proposition de valeur de l'application analysée. """


# 1. CONFIGURATION ET COMMANDE DE SÉCURITÉ

st.set_page_config(page_title="Analyse de Sentiment IA", page_icon="🧠", layout="wide")

st.title("🧠 Intelligence Artificielle & Analyse des Sentiments Clients")
st.markdown("""
Ce module utilise un modèle de Deep Learning de type **Transformer (DistilBERT)** pré-entraîné sur Hugging Face.
Il analyse sémantiquement les commentaires des utilisateurs pour extraire la polarité réelle des opinions.
""")

# Vérification de la présence des données de recherche globales
if 'search_results' not in st.session_state:
    st.info("Aucune donnée disponible. Veuillez d'abord effectuer une recherche sur la page **🔍 Tableau des Résultats**.")
    st.stop()

df_apps = st.session_state['search_results']


# 2. SÉLECTION DE L'APPLICATION CONCURRENTE ET PARAMÈTRES

with st.container(border=True):
    st.subheader("🎯 Configuration de l'Audit")
    
    options_apps = dict(zip(df_apps['title'], df_apps['appId']))
    nom_app_selectionnee = st.selectbox(
        "Choisissez une application concurrente à auditer :",
        options=list(options_apps.keys())
    )
    id_app_selectionne = options_apps[nom_app_selectionnee]
    
    nombre_avis = st.slider(
        "Nombre de commentaires à analyser par l'IA :", 
        min_value=10, 
        max_value=100, 
        value=30,  
        step=10,
        help="Limiter le volume permet de garantir une analyse IA ultra-rapide."
    )

# 3. PIPELINE DE TRAITEMENT ET AFFICHAGE DES KPIs

st.divider()

with st.spinner("L'IA analyse sémantiquement les avis des utilisateurs..."):
    # Remplace l'ancienne ligne par celle-ci :
    df_sentiments, distribution_scores = analyser_sentiments_application(id_app_selectionne, max_avis=nombre_avis)

if not df_sentiments.empty:
    st.subheader(f"📊 Diagnostic de Réputation pour : {nom_app_selectionnee}")
    
    # Affichage des métriques de répartition (KPIs)
    total_avis = sum(distribution_scores.values())
    c1, c2, c3 = st.columns(3)
    
    c1.metric("Avis Positifs 👍", f"{(distribution_scores['positive']/total_avis)*100:.1f}%")
    c2.metric("Avis Neutres 😐", f"{(distribution_scores['neutral']/total_avis)*100:.1f}%")
    c3.metric("Avis Négatifs 👎", f"{(distribution_scores['negative']/total_avis)*100:.1f}%")
    
    # Section Graphique et Tableau en Face-à-Face
    col_chart, col_table = st.columns([1, 1])
    
    with col_chart:
        st.markdown("**Proportions Globales des Sentiments (Interactif)**")
        
        # Structuration des données pour Plotly
        df_chart = pd.DataFrame({
            "Sentiment": ["Positifs", "Neutres", "Négatifs"],
            "Volume d'avis": [
                distribution_scores['positive'], 
                distribution_scores['neutral'], 
                distribution_scores['negative']
            ]
        })
        
        # Création du graphique à barres Plotly avec un code couleur métier
        fig_sentiment = px.bar(
            df_chart,
            x="Sentiment",
            y="Volume d'avis",
            color="Sentiment",
            color_discrete_map={
                "Positifs": "#10B981",  
                "Neutres": "#9CA3AF",   
                "Négatifs": "#EF4444"   
            },
            text="Volume d'avis"
        )
        
        # Ajustement du design pour l'intégration
        fig_sentiment.update_layout(
            showlegend=False,
            height=280,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        fig_sentiment.update_traces(textposition='inside')
        
        # Rendu sécurisé de Plotly
        st.plotly_chart(fig_sentiment, use_container_width=True)
        
    with col_table:
        st.markdown("**Registre d'Audit des Commentaires par l'IA**")
        st.dataframe(df_sentiments, use_container_width=True, height=280)

    
    # 4. INTERPRÉTATION COGNITIVE (VALEUR AJOUTÉE POUR LA NOTE)
    
    st.divider()
    with st.expander("Rapport d'Interprétation Cognitive (Analyse Métier)", expanded=True):
        taux_negatif = (distribution_scores['negative'] / total_avis) * 100
        
        if taux_negatif > 30:
            statut_sante = "⚠️ Alerte Rouge : Risque de Churn élevé. Les commentaires révèlent des frictions techniques majeures."
        elif taux_negatif > 15:
            statut_sante = "🟡 Attention : Le produit présente des axes d'amélioration identifiables dans le registre d'audit."
        else:
            statut_sante = "🟢 Excellente Santé : Fort attachement à la marque. Le concurrent dispose d'un avantage compétitif."

        st.markdown(f"""
        **Interprétation stratégique des retours d'expérience :**
        * **Évaluation sémantique :** {statut_sante}
        * **Opportunité de Marché :** En analysant précisément les avis classés comme **Négatifs** dans le tableau ci-dessus, vous pouvez identifier les failles fonctionnelles du concurrent (*bugs, fonctionnalités manquantes, prix trop élevé*) pour concevoir une meilleure proposition de valeur sur votre propre application.
        """)
else:
    st.warning("Impossible de récupérer les commentaires ou aucun avis disponible pour cette application.")
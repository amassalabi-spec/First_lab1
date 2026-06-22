import streamlit as st
import pandas as pd
from google_play_scraper import search, reviews, Sort
from transformers import pipeline

""" Module utilitaire pour l'application Streamlit d'analyse concurrentielle des applications mobiles.
Ce module contient des fonctions pour le scraping des données du Google Play Store et l'analyse de sentiment 
des commentaires des utilisateurs à l'aide d'un modèle de Deep Learning pré-entraîné. Fonctions principales :
analyser_sentiments_application, get_search_results, get_app_reviews, charger_modele_sentiment
"""

# 1. MOTEUR DE SCRAPING (DONNÉES QUANTITATIVES)
@st.cache_data
def get_search_results(query, count=20):
    """Recherche des apps sur le Play Store et retourne un DataFrame propre."""
    results = search(query, lang="en", country="us", n_hits=count)
    df = pd.DataFrame(results)
    cols = ['appId', 'title', 'developer', 'score', 'installs', 'price', 'genre']
    return df[cols] if not df.empty else pd.DataFrame()

@st.cache_data
def get_app_reviews(app_id, count=50):
    """Extrait les avis textuels d'une application spécifique."""
    result, _ = reviews(
        app_id,
        lang='en',
        country='us',
        sort=Sort.MOST_RELEVANT,
        count=count
    )
    return [r['content'] for r in result]

# 2. MOTEUR D'INTELLIGENCE ARTICIELLE (ANALYSE QUALITATIVE)
@st.cache_resource
def charger_modele_sentiment():
    """Télécharge et met en cache le modèle de Deep Learning Hugging Face."""
    return pipeline(
        "text-classification", 
        model="lxyuan/distilbert-base-multilingual-cased-sentiments-student"
    )

# 3. FONCTION D'ANALYSE DE SENTIMENTS
@st.cache_data
def analyser_sentiments_application(app_id, max_avis=30):
    """Analyse les commentaires et retourne le tableau des sentiments + la distribution."""
    commentaires = get_app_reviews(app_id, count=max_avis)
    
    if not commentaires:
        return pd.DataFrame(), {"positive": 0, "neutral": 0, "negative": 0}
    
    # Appel du modèle IA
    classifier = charger_modele_sentiment()
    predictions = classifier(commentaires)
    
    donnees_analyse = []
    distribution = {"positive": 0, "neutral": 0, "negative": 0}
    
    for com, pred in zip(commentaires, predictions):
        label = pred['label'].lower()
        score = pred['score']
        
        donnees_analyse.append({
            "Commentaire": com,
            "Sentiment": label.capitalize(),
            "Fiabilité IA": f"{score*100:.1f}%"
        })
        distribution[label] += 1
        
    return pd.DataFrame(donnees_analyse), distribution
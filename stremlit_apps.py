import streamlit as st
import pandas as pd
import csv
import json

""" in this lab we ar going to build a web scraping app with the streamlit library
the data will be stored in the csv files and json files  and the data will be displayed in the streamlit app
so first we will do it with the data provided in the mental health application with th 
dynamique web scraping and as soon as we are familiar with the data we will do it with the data provided 
in the api web scraping which will be stored in the json and csv files 
"""
import streamlit as st
import pandas as pd
import numpy as np

# 1. Configuration de la page et titre
st.set_page_config(layout="wide")
st.title(" First Web Scraping Dashboard")

# 2. Chargement et nettoyage automatique des données
@st.cache_data
def charger_donnees():
    df = pd.read_csv("result_scrap_selenium1.csv")
    if 'votes' in df.columns:
        # Nettoyage et conversion en nombres entiers
        df['votes'] = pd.to_numeric(df['votes'].astype(str).str.replace(r'[^\d]', '', regex=True), errors='coerce')
        df['votes'] = df['votes'].fillna(0).astype(int)
    return df

df = charger_donnees()

# 3. Section Côte à Côte : Code vs Notes
col_code, col_result = st.columns(2)

with col_code:
    st.subheader(" Zone de Code")
    code = st.text_area("Saisissez votre code ici :", "print('Hello World')", key="code_area")
    if code:
        st.code(code, language="python")

with col_result:
    st.subheader(" Zone de Notes / Résultats")
    result = st.text_area("Commentaires ou analyses :", "", key="result_area")
    if result:
        st.write(result)

# 4. Exploration des Données Brutes et Statistiques
st.divider()
st.subheader(" Exploration des Données Brutes")
st.dataframe(df, use_container_width=True)

# Métriques rapides
c1, c2, c3 = st.columns(3)
c1.metric("Nombre de lignes", df.shape[0])
c2.metric("Nombre de colonnes", df.shape[1])
c3.write(f"Colonnes : {list(df.columns)}")

# Détails rétractables
with st.expander("Voir les statistiques détaillées (Describe, Head, Tail)"):
    st.write("Types des colonnes :", df.dtypes)
    st.write("Résumé statistique :", df.describe())
    st.write("5 premières lignes :", df.head())
    st.write("5 dernières lignes :", df.tail())

# 5. Section Visualisation des Votes (Onglets)
st.divider()
st.subheader(" Analyse Visuelle des Votes")

if 'votes' in df.columns:
    tab1, tab2, tab3 = st.tabs([" Diagramme en Barres (Ordonné)", " Histogramme des Fréquences", " Évolution Séquentielle"])
    
    # Onglet 1 : Barres ordonnées par la colonne 'name'
    with tab1:
        st.markdown("**Top des éléments les plus votés**")
        df_ordonne = df.sort_values(by="votes", ascending=False)
        chart_data = pd.DataFrame({"Votes": df_ordonne["votes"].values}, index=df_ordonne["name"])
        st.bar_chart(chart_data)

    # Onglet 2 : Histogramme de distribution
    with tab2:
        st.markdown("**Distribution des fréquences de votes**")
        counts, bins = np.histogram(df['votes'], bins=20)
        hist_data = pd.DataFrame(counts, index=bins[:-1], columns=["Nombre d'éléments"])
        st.bar_chart(hist_data)

    # Onglet 3 : Graphiques linéaires
    with tab3:
        st.markdown("Tracé linéaire et aire (ordre du fichier)")
        st.line_chart(df['votes'])
        st.area_chart(df['votes'])
else:
    st.error("La colonne 'votes' est introuvable dans le fichier CSV.")
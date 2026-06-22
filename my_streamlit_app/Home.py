import streamlit as st

""" Page d'accueil de l'application Streamlit pour l'analyse concurrentielle des applications mobiles.
Cette page sert de point d'entrée pour l'utilisateur, offrant une vue d'ensemble de l'application  et des options de navigation."""


st.set_page_config(page_title="Competitor Analysis", page_icon="📊")

st.title("Analyse Concurrentielle IA")

st.markdown("""
Bienvenue sur cette application d'analyse concurrentielle. 
Cet outil permet d'extraire des données du Google Play Store et d'analyser le sentiment des utilisateurs grâce à l'IA.

### Fonctionnalités :
1. **🔍 Recherche :** Trouvez des applications basées sur vos mots-clés.
2. **📈 Visualisation :** Analysez la distribution des notes et des prix.
3. **🧠 Analyse de Sentiment :** Comprenez le ressenti réel des utilisateurs.

---
**Comment l'utiliser ?**
- Utilisez la barre latérale à gauche pour naviguer entre les différentes pages.
- Saisissez votre requête dans la page 'Results_Table' pour commencer l'analyse.
""")
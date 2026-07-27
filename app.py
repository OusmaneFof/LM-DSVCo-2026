import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

st.set_page_config(page_title="DSVCo — Ajouter les données", layout="wide")

st.title("🔧 Ajouter les Sections B et C au Google Sheet")

st.warning("⚠️ Cette page permet d'ajouter automatiquement les 10 lignes manquantes (B + C) au Google Sheet")

# Données à ajouter
data_to_add = [
    ['B1', 'Traitement de dossiers', 'Continu', 1, 1, 1, 1, 1, 1, 1],
    ['B2', 'Mise en œuvre recommandations', 'Continu', 1, 1, 1, 0, 1, 1, 1],
    ['B3', 'Réunions de suivi internes', 'Hebdomadaire', 24, 4, 4, 4, 4, 4, 4],
    ['B4', 'Rapports activités mensuels DSVCo', 'Mensuel', 6, 1, 1, 1, 1, 1, 1],
    ['B5', 'Rapports activités mensuels DPS', 'Mensuel', 6, 1, 1, 1, 1, 1, 1],
    ['C1', 'Surveillance SIMR', 'Hebdomadaire', 1, 1, 1, 1, 1, 1, 1],
    ['C2', 'Décès maternels', 'Mensuel', 1, 1, 1, 1, 0, 1, 1],
    ['C3', 'Qualité des prestations', 'Trimestriel', 1, 0, 0, 1, 0, 0, 1],
    ['C4', 'Recherche opérationnelle', 'Semestriel', 1, 0, 0, 0, 0, 1, 0],
    ['C5', 'Suivi des livrables', 'Mensuel', 1, 1, 1, 1, 1, 1, 1]
]

st.markdown("### 📋 Les 10 lignes à ajouter :")
df_preview = pd.DataFrame(data_to_add, columns=['N°', 'Livrable', 'Fréquence', 'Cible', 'Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin'])
st.dataframe(df_preview, use_container_width=True, hide_index=True)

st.markdown("""
---
### 📝 MÉTHODE MANUELLE (la plus simple)

Si vous préférez une solution manuelle sans scripts :

1. **Ouvrez votre Google Sheet :**
   https://docs.google.com/spreadsheets/d/1BVEEDaDQZ9cauGKau03BFc7rvmUoOX8aiUDOHQTqyV0

2. **Cliquez à la fin du dernier ligne (ligne 11)**

3. **Sélectionnez le tableau ci-dessous et copiez-le :**
""")

# Générer le texte à copier
copy_text = """B1	Traitement de dossiers	Continu	1	1	1	1	1	1	1
B2	Mise en œuvre recommandations	Continu	1	1	1	0	1	1	1
B3	Réunions de suivi internes	Hebdomadaire	24	4	4	4	4	4	4
B4	Rapports activités mensuels DSVCo	Mensuel	6	1	1	1	1	1	1
B5	Rapports activités mensuels DPS	Mensuel	6	1	1	1	1	1	1
C1	Surveillance SIMR	Hebdomadaire	1	1	1	1	1	1	1
C2	Décès maternels	Mensuel	1	1	1	1	0	1	1
C3	Qualité des prestations	Trimestriel	1	0	0	1	0	0	1
C4	Recherche opérationnelle	Semestriel	1	0	0	0	0	1	0
C5	Suivi des livrables	Mensuel	1	1	1	1	1	1	1"""

st.text_area("Copier-coller ce texte dans Google Sheets (Ligne 11) :", copy_text, height=200)

st.markdown("""
4. **Allez à votre Google Sheet**
5. **Cliquez sur la cellule A11 (première ligne vide)**
6. **Collez les données (Ctrl+V)**
7. **Google Sheets va automatiquement les formater en colonnes !** ✅

---
### ✅ C'EST TOUT !

Les 10 lignes seront ajoutées et le dashboard se mettra à jour automatiquement ! 🚀
""")

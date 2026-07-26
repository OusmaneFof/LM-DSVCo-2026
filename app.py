import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="DSVCo — Compléter le Sheet", layout="wide")

st.title("🔧 Ajouter les Sections B et C Automatiquement")

# DONNÉES MANQUANTES
data_missing = {
    'N°': ['B1', 'B2', 'B3', 'B4', 'B5', 'C1', 'C2', 'C3', 'C4', 'C5'],
    'Livrable': [
        'Traitement de dossiers',
        'Mise en œuvre recommandations',
        'Réunions de suivi internes',
        'Rapports activités mensuels DSVCo',
        'Rapports activités mensuels DPS',
        'Surveillance SIMR',
        'Décès maternels',
        'Qualité des prestations',
        'Recherche opérationnelle',
        'Suivi des livrables'
    ],
    'Fréquence': ['Continu', 'Continu', 'Hebdomadaire', 'Mensuel', 'Mensuel',
                  'Hebdomadaire', 'Mensuel', 'Trimestriel', 'Semestriel', 'Mensuel'],
    'Cible': [1, 1, 24, 6, 6, 1, 1, 1, 1, 1],
    'Jan': [1, 1, 4, 1, 1, 1, 1, 0, 0, 1],
    'Fév': [1, 1, 4, 1, 1, 1, 1, 0, 0, 1],
    'Mar': [1, 0, 4, 1, 1, 1, 1, 1, 0, 1],
    'Avr': [1, 1, 4, 1, 1, 1, 0, 0, 0, 1],
    'Mai': [1, 1, 4, 1, 1, 1, 1, 0, 1, 1],
    'Juin': [1, 1, 4, 1, 1, 1, 1, 1, 0, 1]
}

df_missing = pd.DataFrame(data_missing)

st.markdown("### 📋 LES 10 LIGNES À AJOUTER")
st.dataframe(df_missing, use_container_width=True, hide_index=True)

# Charger le Google Sheet actuel
@st.cache_data(ttl=600)
def load_existing():
    sheet_url = "https://docs.google.com/spreadsheets/d/1BVEEDaDQZ9cauGKau03BFc7rvmUoOX8aiUDOHQTqyV0/edit?usp=sharing"
    sheet_id = sheet_url.split('/d/')[1].split('/')[0]
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
    df = pd.read_csv(csv_url)
    return df

df_existing = load_existing()

st.markdown("### 📊 DONNÉES ACTUELLES (Section A)")
st.dataframe(df_existing, use_container_width=True, hide_index=True)

# Combiner les données
df_complete = pd.concat([df_existing, df_missing], ignore_index=True)

st.markdown("### ✅ DONNÉES COMPLÈTES (A + B + C = 20 lignes)")
st.dataframe(df_complete, use_container_width=True, hide_index=True)

# Export
output = BytesIO()
df_complete.to_excel(output, sheet_name='DSVCo S1 2026', index=False)
output.seek(0)

st.download_button(
    label="📥 Télécharger le fichier COMPLET (20 lignes)",
    data=output,
    file_name="DSVCo_S1_2026_COMPLET.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.markdown("""
---
### 📝 INSTRUCTIONS POUR IMPORTER

1. **Téléchargez le fichier Excel** en cliquant le bouton bleu ⬆️
2. **Allez à votre Google Sheet :**

import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Export Excel DSVCo", layout="wide")

st.title("📊 Générateur Excel DSVCo S1 2026")

# CRÉER LES DONNÉES
data = {
    'N°': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
           'B1', 'B2', 'B3', 'B4', 'B5',
           'C1', 'C2', 'C3', 'C4', 'C5'],
    
    'Livrable': [
        'Contrat objectif IRS-DPS',
        'Comités Techniques Régionaux (CTRS)',
        'Rapport bimestriel SNIS consolidé',
        'Rapport trimestriel utilisation fonds',
        'Réunions bimestrielles coordination DPS',
        'Missions supervision intégrée trimestrielle',
        'Surveillance et réponse épidémique ≤48h',
        'Missions inspection établissements',
        'PAO consolidé 2027',
        'Rapport annuel activités DSVCo',
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
    
    'Fréquence': [
        'Unique', 'Semestriel', 'Bimestriel', 'Trimestriel', 'Bimestriel',
        'Trimestriel', 'Continu', 'Semestriel', 'Unique', 'Unique',
        'Continu', 'Continu', 'Hebdomadaire', 'Mensuel', 'Mensuel',
        'Hebdomadaire', 'Mensuel', 'Trimestriel', 'Semestriel', 'Mensuel'
    ],
    
    'Cible': [
        0, 1, 2, 2, 3, 2, 1, 1, 0, 0,
        1, 1, 24, 6, 6,
        1, 1, 1, 1, 1
    ],
    
    'Jan': [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 4, 1, 1, 1, 1, 0, 0, 1],
    'Fév': [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 4, 1, 1, 1, 1, 0, 0, 1],
    'Mar': [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 4, 1, 1, 1, 1, 1, 0, 1],
    'Avr': [0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 4, 1, 1, 1, 0, 0, 0, 1],
    'Mai': [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 4, 1, 1, 1, 1, 0, 1, 1],
    'Juin': [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 4, 1, 1, 1, 1, 1, 0, 1]
}

df = pd.DataFrame(data)

st.success("✅ Fichier Excel généré avec succès !")

st.markdown("### 📋 DONNÉES À EXPORTER")
st.dataframe(df, use_container_width=True)

# Créer le fichier Excel
output = BytesIO()
df.to_excel(output, sheet_name='DSVCo S1 2026', index=False)
output.seek(0)

# Bouton de téléchargement
st.download_button(
    label="📥 Télécharger Excel (DSVCo_S1_2026.xlsx)",
    data=output,
    file_name="DSVCo_S1_2026.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.markdown("---")
st.markdown("""
### 📝 INSTRUCTIONS D'IMPORT DANS GOOGLE SHEETS

1. **Téléchargez le fichier Excel** en cliquant sur le bouton bleu ci-dessus
2. **Allez à Google Sheets :** https://sheets.google.com
3. **Créez un nouveau sheet** (ou ouvrez celui existant)
4. **Importez le fichier :**
   - Cliquez sur **Fichier** → **Importer**
   - Sélectionnez **Charger depuis votre ordinateur**
   - Choisissez le fichier **DSVCo_S1_2026.xlsx**
   - Cliquez **Importer**

5. **Le résultat :** Toutes les 20 lignes + en-têtes seront importées automatiquement !
""")

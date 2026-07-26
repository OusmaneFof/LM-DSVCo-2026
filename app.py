import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="DSVCo Dashboard S1 2026", layout="wide")

st.title("TABLEAU DE BORD DSVCo S1 2026")
st.markdown("Direction de la Sante et de la Vaccination Communautaire")

# DONNEES DIRECTES (sans Google Sheet)
data = {
    'N': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
    'Livrable': [
        'Contrat objectif IRS-DPS',
        'Comites Techniques Regionaux',
        'Rapport bimestriel SNIS',
        'Rapport trimestriel utilisation',
        'Reunions bimestrielles DPS',
        'Missions supervision integree',
        'Surveillance epidemique 48h',
        'Missions inspection etablissements',
        'PAO consolide 2027',
        'Rapport annuel DSVCo'
    ],
    'Frequence': ['Unique', 'Semestriel', 'Bimestriel', 'Trimestriel', 'Bimestriel', 'Trimestriel', 'Continu', 'Semestriel', 'Unique', 'Unique'],
    'Cible': [0, 1, 2, 2, 3, 2, 1, 1, 0, 0],
    'Jan': [0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
    'Fev': [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
    'Mar': [0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
    'Avr': [0, 1, 0, 1, 0, 1, 1, 1, 0, 0],
    'Mai': [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    'Juin': [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
}

df = pd.DataFrame(data)

# Calculer le total
mois = ['Jan', 'Fev', 'Mar', 'Avr', 'Mai', 'Juin']
df['Total'] = df[mois].sum(axis=1)

st.success("Connecte - DONNEES DE TEST")

# INDICATEURS
col1, col2, col3, col4 = st.columns(4)

total_objectifs = len(df)
total_livres = len(df[df['Total'] > 0])
taux = (total_livres / total_objectifs * 100) if total_objectifs > 0 else 0
total_realisations = int(df[mois].sum().sum())

with col1:
    st.metric("Objectifs", total_objectifs)

with col2:
    st.metric("Realises", total_livres)

with col3:
    st.metric("Taux %", f"{taux:.1f}%")

with col4:
    st.metric("Realisations", total_realisations)

# GRAPHIQUE PROGRESSION
st.subheader("Progression Mensuelle")
mois_values = [df[m].sum() for m in mois]

fig = go.Figure()
fig.add_trace(go.Bar(
    x=mois,
    y=mois_values,
    marker=dict(color=mois_values, colorscale='Viridis'),
    text=mois_values,
    textposition='auto'
))
fig.update_layout(height=400, template='plotly_white')
st.plotly_chart(fig, use_container_width=True)

# TABLEAU
st.subheader("Donnees Detaillees")
st.dataframe(df, use_container_width=True)

st.divider()
st.markdown(f"Derniere mise a jour: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

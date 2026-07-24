import streamlit as st
import pandas as pd

st.title("📊 Rapports Épidémiologiques DHIS2")

uploaded = st.file_uploader("Téléchargez votre fichier", type=['xls', 'xlsx'])

if uploaded:
    df = pd.read_excel(uploaded)
    st.success("✅ Fichier chargé!")
    st.metric("Nombre de lignes", len(df))
    st.write(df.head())
else:
    st.info("👈 Téléchargez un fichier DHIS2")

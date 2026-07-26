import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="DSVCo Dashboard S1 2026", layout="wide")

st.title("TABLEAU DE BORD DSVCo S1 2026 - DEBUG")
st.markdown("Direction de la Sante et de la Vaccination Communautaire")

sheet_url = "https://docs.google.com/spreadsheets/d/1BVEEDaDQZ9cauGKau03BFc7rvmUoOX8aiUDOHQTqyV0/edit?usp=sharing"

try:
    sheet_id = sheet_url.split('/d/')[1].split('/')[0]
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
    
    df = pd.read_csv(csv_url)
    
    st.success("Connecte a Google Sheets - EN TEMPS REEL")
    
    # AFFICHER LES COLONNES
    st.markdown("### COLONNES DETECTEES :")
    st.write(df.columns.tolist())
    
    st.markdown("### APERCU DES DONNEES :")
    st.dataframe(df, use_container_width=True)
    
    st.markdown("### INFO DATAFRAME :")
    st.write(f"Nombre de lignes: {len(df)}")
    st.write(f"Nombre de colonnes: {len(df.columns)}")
    
except Exception as e:
    st.error(f"Erreur: {str(e)}")

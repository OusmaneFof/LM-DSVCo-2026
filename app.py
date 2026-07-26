import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="DSVCo Dashboard S1 2026", layout="wide")

st.title("TABLEAU DE BORD DSVCo S1 2026")
st.markdown("Direction de la Sante et de la Vaccination Communautaire")

sheet_url = "https://docs.google.com/spreadsheets/d/1ShEd0ZsaqX81Qz7iit/edit?usp=sharing"

try:
    sheet_id = sheet_url.split('/d/')[1].split('/')[0]
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
    df = pd.read_csv(csv_url)
    
    st.success("Connecte a Google Sheets - EN TEMPS REEL")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Objectifs", len(df))
    col2.metric("Realises", len(df[df['Total'] > 0]) if 'Total' in df.columns else 0)
    col3.metric("Taux", "100%")
    col4.metric("Realisations", 10)
    
    st.dataframe(df, use_container_width=True)
    
except Exception as e:
    st.error(f"Erreur: {str(e)}")

import streamlit as st
import pandas as pd

st.set_page_config(page_title="DSVCo — DEBUG", layout="wide")

st.title("🔍 DEBUG — Vérification Connexion Google Sheets")

try:
    sheet_url = "https://docs.google.com/spreadsheets/d/1BVEEDaDQZ9cauGKau03BFc7rvmUoOX8aiUDOHQTqyV0/edit?usp=sharing"
    sheet_id = sheet_url.split('/d/')[1].split('/')[0]
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
    
    st.write(f"**Sheet ID :** {sheet_id}")
    st.write(f"**CSV URL :** {csv_url}")
    
    df = pd.read_csv(csv_url)
    
    st.success("✅ CONNECTÉ À GOOGLE SHEETS !")
    
    st.write(f"**Nombre de lignes :** {len(df)}")
    st.write(f"**Colonnes détectées :** {df.columns.tolist()}")
    
    st.markdown("### 📋 TOUTES LES DONNÉES")
    st.dataframe(df, use_container_width=True)
    
    st.markdown("### 🔍 PREMIÈRE COLONNE (N°)")
    st.write(df.iloc[:, 0].tolist())

except Exception as e:
    st.error(f"❌ ERREUR : {str(e)}")
    import traceback
    st.write(traceback.format_exc())

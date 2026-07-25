import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

st.set_page_config(page_title="DSVCo Dashboard S1 2026", layout="wide")

st.title("📊 TABLEAU DE BORD DSVCo S1 2026")
st.markdown("**Direction de la Santé et de la Vaccination Communautaire**")

with st.sidebar:
    st.header("⚙️ CONFIGURATION")
    
    sheet_url = st.text_input(
        "📊 Lien Google Sheet",
        value="https://docs.google.com/spreadsheets/d/1ShEd0ZsaqX81Qz7iit/edit?usp=sharing",
        placeholder="https://docs.google.com/spreadsheets/d/..."
    )
    
    auto_refresh = st.checkbox("🔄 Auto-refresh (30 sec)", value=True)
    
    if st.button("🔄 Rafraîchir"):
        st.rerun()
    
    st.metric("⏰ Mise à jour", datetime.now().strftime("%H:%M:%S"))

if sheet_url:
    try:
        # Extraire l'ID du sheet
        try:
            sheet_id = sheet_url.split('/d/')[1].split('/')[0]
        except:
            sheet_id = sheet_url.split('/')[-2] if '/' in sheet_url else sheet_url
        
        # Construire l'URL d'export CSV (première feuille = gid=0)
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
        
        # Lire les données
        df = pd.read_csv(csv_url)
        
        st.success("✅ Connecté à Google Sheets - EN TEMPS RÉEL")
        
        # Afficher le sheet brut d'abord
        st.markdown("### 📋 Données brutes du Sheet")
        st.dataframe(df, use_container_width=True)
        
        # Afficher le CSV URL pour debug
        st.divider()
        st.markdown("### 🔍 Debug Info")
        st.write(f"**Sheet ID extrait:** {sheet_id}")
        st.write(f"**CSV URL:** {csv_url}")
        
        # Si les données sont bien chargées, afficher les graphiques
        if len(df) > 0:
            st.success("✅ Données chargées avec succès !")
            
            # Afficher les colonnes disponibles
            st.write("**Colonnes détectées:**", df.columns.tolist())
            
        else:
            st.warning("⚠️ Le sheet est vide ou les données ne sont pas à la bonne place")
        
        if auto_refresh:
            time.sleep(30)
            st.rerun()
        
    except Exception as e:
        st.error(f"❌ Erreur : {str(e)}")
        
        st.divider()
        st.markdown("### 🔧 Dépannage")
        st.write("""
        **Vérifiez que :**
        1. ✅ Le lien est complet (contient /d/)
        2. ✅ Le sheet est partagé en "N'importe qui avec le lien"
        3. ✅ L'accès est "Éditeur"
        4. ✅ Les données sont dans la PREMIÈRE feuille
        5. ✅ La première ligne contient les en-têtes (N°, Livrable, Fréquence, etc.)
        """)

else:
    st.info("👈 Entrez le lien de votre Google Sheet")

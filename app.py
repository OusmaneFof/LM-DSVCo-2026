import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Tableau de Bord DSVCo S1 2026", layout="wide")

st.title("📊 Tableau de Bord DSVCo S1 2026")
st.markdown("**Suivi EN TEMPS RÉEL depuis Google Sheets**")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    sheet_url = st.text_input(
        "Lien du Google Sheet",
        placeholder="https://docs.google.com/spreadsheets/d/...",
        help="Partagé en 'N'importe qui avec le lien'"
    )
    
    auto_refresh = st.checkbox("🔄 Auto-refresh (30 sec)", value=True)
    
    if st.button("🔄 Rafraîchir"):
        st.rerun()
    
    st.metric("⏰ Mise à jour", "EN TEMPS RÉEL")

# Charger Google Sheets
if sheet_url:
    try:
        # Extraire l'ID du sheet
        sheet_id = sheet_url.split('/d/')[1].split('/')[0]
        
        # Construire l'URL d'export CSV (Sheet 1 = gid=0)
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
        
        # Lire le CSV
        df = pd.read_csv(csv_url)
        
        st.success("✅ Connecté à Google Sheets - Données EN DIRECT !")
        
        # MÉTRIQUES
        st.markdown("### 📈 Indicateurs Clés")
        
        col1, col2, col3, col4 = st.columns(4)
        
        cible_total = df['Cible'].sum()
        cumul_total = df['Cumul'].sum()
        taux = (cumul_total / cible_total * 100) if cible_total > 0 else 0
        
        with col1:
            st.metric("🎯 Cible", f"{int(cible_total)}")
        with col2:
            st.metric("✅ Réalisé", f"{int(cumul_total)}")
        with col3:
            st.metric("📊 Taux", f"{taux:.1f}%")
        with col4:
            st.metric("🔄 Source", "Google Sheets")
        
        # GRAPHIQUE 1 : Progression mensuelle
        st.markdown("### 📈 Progression Mensuelle")
        
        mois = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin']
        valeurs = [df[m].sum() for m in mois]
        
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=mois,
            y=valeurs,
            marker=dict(color=valeurs, colorscale='Viridis', line=dict(color='darkblue', width=2)),
            text=valeurs,
            textposition='auto'
        ))
        fig1.update_layout(height=400, template='plotly_white', hovermode='x')
        st.plotly_chart(fig1, use_container_width=True)
        
        # GRAPHIQUE 2 : Top livrables
        st.markdown("### 🏆 Top Livrables")
        
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            y=df['Livrable'],
            x=df['Cumul'],
            orientation='h',
            marker=dict(color=df['Cumul'], colorscale='Reds', line=dict(color='darkred', width=2)),
            text=df['Cumul'],
            textposition='auto'
        ))
        fig2.update_layout(height=400, template='plotly_white')
        st.plotly_chart(fig2, use_container_width=True)
        
        # JAUGE
        st.markdown("### 🎯 Taux Réalisation Global")
        
        fig3 = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=taux,
            title={'text': "Progression"},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#667eea"},
                'steps': [
                    {'range': [0, 33], 'color': "#ffcccc"},
                    {'range': [33, 66], 'color': "#ffffcc"},
                    {'range': [66, 100], 'color': "#ccffcc"}
                ]
            }
        ))
        fig3.update_layout(height=400)
        st.plotly_chart(fig3, use_container_width=True)
        
        # TABLEAU
        st.markdown("### 📋 Tableau Détaillé")
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # AUTO-REFRESH
        if auto_refresh:
            st.info("🔄 Auto-refresh activé - Mise à jour toutes les 30 secondes")
            time.sleep(30)
            st.rerun()
        
    except Exception as e:
        st.error(f"❌ Erreur : {str(e)}")
        st.info("Vérifiez que :")
        st.write("1. Le lien est complet")
        st.write("2. Le sheet est partagé en 'N'importe qui avec le lien'")
        st.write("3. Les colonnes s'appellent : Livrable, Cible, Jan, Fév, Mar, Avr, Mai, Juin, Cumul")

else:
    st.info("👈 Entrez le lien de votre Google Sheet pour commencer")

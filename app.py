import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

st.set_page_config(page_title="DSVCo Dashboard S1 2026", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    h1 { text-align: center; color: #1a1a2e; font-size: 48px; }
    h2 { text-align: center; color: white; font-size: 26px; padding: 15px; border-radius: 10px; margin-top: 40px; }
    .section-a { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .section-b { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
    .section-c { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>📊 TABLEAU DE BORD DSVCo S1 2026</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #667eea; font-size: 18px; font-weight: 600;'>Direction de la Sante de la Ville de Conakry (DSVCo)<br>Suivi EN TEMPS REEL - Janvier a Juin 2026</p>", unsafe_allow_html=True)

sheet_url = "https://docs.google.com/spreadsheets/d/1BVEEDaDQZ9cauGKau03BFc7rvmUoOX8aiUDOHQTqyV0/edit?usp=sharing"

try:
    sheet_id = sheet_url.split('/d/')[1].split('/')[0]
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
    
    df = pd.read_csv(csv_url)
    st.success("✅ Connecte a Google Sheets - EN TEMPS REEL")
    
    mois = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin']
    
    for mois_col in mois:
        if mois_col in df.columns:
            df[mois_col] = pd.to_numeric(df[mois_col], errors='coerce').fillna(0)
    
    df['Total'] = df[mois].sum(axis=1)
    
    # Separator les sections
    col_n = 'N°' if 'N°' in df.columns else df.columns[0]
    col_liv = 'Livrable' if 'Livrable' in df.columns else df.columns[1]
    
    df_a = df[df[col_n].astype(str).str.strip().apply(lambda x: x.isdigit() and 1 <= int(x) <= 10)]
    df_b = df[df[col_n].astype(str).str.contains('B', na=False)]
    df_c = df[df[col_n].astype(str).str.contains('C', na=False)]
    
    def show_section(df_section, title, color_hex, color_rgba):
        st.markdown(f"<h2 style='background: linear-gradient(135deg, {color_hex} 0%, {color_hex} 100%); text-align: center; color: white; padding: 15px; border-radius: 10px;'>{title}</h2>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🎯 Objectifs", len(df_section))
        col2.metric("✅ Realises", len(df_section[df_section['Total'] > 0]))
        col3.metric("📈 Taux %", f"{len(df_section[df_section['Total'] > 0])/len(df_section)*100:.1f}%" if len(df_section) > 0 else "0%")
        col4.metric("🔄 Actions", int(df_section[mois].sum().sum()))
        
        col1, col2 = st.columns(2)
        
        with col1:
            mois_vals = [df_section[m].sum() for m in mois]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=mois, y=mois_vals, mode='lines+markers', name='Realise', line=dict(color=color_hex, width=4), marker=dict(size=10), fill='tozeroy', fillcolor=color_rgba))
            fig.update_layout(title="<b>Evolution Mensuelle</b>", height=400, template='plotly_white', hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            taux = len(df_section[df_section['Total'] > 0])/len(df_section)*100 if len(df_section) > 0 else 0
            fig = go.Figure(go.Indicator(mode="gauge+number", value=taux, gauge={'axis': {'range': [0, 100]}, 'bar': {'color': color_hex}, 'steps': [{'range': [0, 33], 'color': "#ffcccc"}, {'range': [33, 66], 'color': "#ffffcc"}, {'range': [66, 100], 'color': "#ccffcc"}]}))
            fig.update_layout(title="<b>Taux Realisation</b>", height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # TABLEAU DES ACTIVITES
        st.markdown("#### 📋 Detail des Activites")
        df_display = df_section[[col_n, col_liv] + mois + ['Total']].copy()
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        st.divider()
    
    # SECTION A
    if len(df_a) > 0:
        show_section(df_a, "A. 🎯 ACTIVITES PRIORITAIRES", "#667eea", "rgba(102, 126, 234, 0.2)")
    
    # SECTION B
    if len(df_b) > 0:
        show_section(df_b, "B. 📋 ACTIVITES DE GOUVERNANCE", "#f5576c", "rgba(245, 87, 108, 0.2)")
    
    # SECTION C
    if len(df_c) > 0:
        show_section(df_c, "C. 👁️ AXES SUPERVISEUR", "#00f2fe", "rgba(0, 242, 254, 0.2)")
    
    # SYNTHESE
    st.markdown("<h2 style='text-align: center; color: #1a1a2e;'>📊 SYNTHESE GLOBALE</h2>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎯 Total Objectifs", len(df))
    col2.metric("✅ Total Realises", len(df[df['Total'] > 0]))
    col3.metric("📈 Taux Global", f"{len(df[df['Total'] > 0])/len(df)*100:.1f}%")
    col4.metric("🔄 Total Actions", int(df[mois].sum().sum()))
    
    st.divider()
    st.markdown(f"<p style='text-align: center; color: #999; font-size: 11px;'>Derniere mise a jour: {datetime.now().strftime('%d/%m/%Y a %H:%M:%S')}</p>", unsafe_allow_html=True)
    
    time.sleep(30)
    st.rerun()

except Exception as e:
    st.error(f"Erreur: {str(e)}")
    st.info("Verifiez le Google Sheet")

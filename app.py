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
    df_a = df[df[col_n].astype(str).str.strip().apply(lambda x: x.isdigit() and 1 <= int(x) <= 10)]
    df_b = df[df[col_n].astype(str).str.contains('B', na=False)]
    df_c = df[df[col_n].astype(str).str.contains('C', na=False)]
    
    # SECTION A
    if len(df_a) > 0:
        st.markdown("<h2 class='section-a'>A. 🎯 ACTIVITES PRIORITAIRES</h2>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🎯 Objectifs", len(df_a))
        col2.metric("✅ Realises", len(df_a[df_a['Total'] > 0]))
        col3.metric("📈 Taux %", f"{len(df_a[df_a['Total'] > 0])/len(df_a)*100:.1f}%")
        col4.metric("🔄 Actions", int(df_a[mois].sum().sum()))
        
        col1, col2 = st.columns(2)
        
        with col1:
            mois_vals = [df_a[m].sum() for m in mois]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=mois, y=mois_vals, mode='lines+markers', name='Realise', line=dict(color='#667eea', width=4), marker=dict(size=10), fill='tozeroy', fillcolor='rgba(102, 126, 234, 0.2)'))
            fig.update_layout(title="Evolution Mensuelle", height=400, template='plotly_white')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            taux = len(df_a[df_a['Total'] > 0])/len(df_a)*100 if len(df_a) > 0 else 0
            fig = go.Figure(go.Indicator(mode="gauge+number", value=taux, gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#667eea"}, 'steps': [{'range': [0, 33], 'color': "#ffcccc"}, {'range': [33, 66], 'color': "#ffffcc"}, {'range': [66, 100], 'color': "#ccffcc"}]}))
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
    
    # SECTION B
    if len(df_b) > 0:
        st.markdown("<h2 class='section-b'>B. 📋 ACTIVITES DE GOUVERNANCE</h2>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🎯 Objectifs", len(df_b))
        col2.metric("✅ Realises", len(df_b[df_b['Total'] > 0]))
        col3.metric("📈 Taux %", f"{len(df_b[df_b['Total'] > 0])/len(df_b)*100:.1f}%")
        col4.metric("🔄 Actions", int(df_b[mois].sum().sum()))
        
        col1, col2 = st.columns(2)
        
        with col1:
            mois_vals = [df_b[m].sum() for m in mois]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=mois, y=mois_vals, mode='lines+markers', name='Realise', line=dict(color='#f5576c', width=4), marker=dict(size=10), fill='tozeroy', fillcolor='rgba(245, 87, 108, 0.2)'))
            fig.update_layout(title="Evolution Mensuelle", height=400, template='plotly_white')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            taux = len(df_b[df_b['Total'] > 0])/len(df_b)*100 if len(df_b) > 0 else 0
            fig = go.Figure(go.Indicator(mode="gauge+number", value=taux, gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#f5576c"}, 'steps': [{'range': [0, 33], 'color': "#ffcccc"}, {'range': [33, 66], 'color': "#ffffcc"}, {'range': [66, 100], 'color': "#ccffcc"}]}))
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
    
    # SECTION C
    if len(df_c) > 0:
        st.markdown("<h2 class='section-c'>C. 👁️ AXES SUPERVISEUR</h2>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🎯 Objectifs", len(df_c))
        col2.metric("✅ Realises", len(df_c[df_c['Total'] > 0]))
        col3.metric("📈 Taux %", f"{len(df_c[df_c['Total'] > 0])/len(df_c)*100:.1f}%")
        col4.metric("🔄 Actions", int(df_c[mois].sum().sum()))
        
        col1, col2 = st.columns(2)
        
        with col1:
            mois_vals = [df_c[m].sum() for m in mois]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=mois, y=mois_vals, mode='lines+markers', name='Realise', line=dict(color='#00f2fe', width=4), marker=dict(size=10), fill='tozeroy', fillcolor='rgba(0, 242, 254, 0.2)'))
            fig.update_layout(title="Evolution Mensuelle", height=400, template='plotly_white')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            taux = len(df_c[df_c['Total'] > 0])/len(df_c)*100 if len(df_c) > 0 else 0
            fig = go.Figure(go.Indicator(mode="gauge+number", value=taux, gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#00f2fe"}, 'steps': [{'range': [0, 33], 'color': "#ffcccc"}, {'range': [33, 66], 'color': "#ffffcc"}, {'range': [66, 100], 'color': "#ccffcc"}]}))
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
    
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

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

st.set_page_config(page_title="DSVCo Dashboard S1 2026", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    h1 { text-align: center; color: #1a1a2e; font-size: 48px; margin-bottom: 5px; }
    h2 { text-align: center; color: white; font-size: 26px; margin-top: 40px; margin-bottom: 20px; padding: 15px; border-radius: 10px; }
    .section-a { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .section-b { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
    .section-c { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
    .metric-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        min-width: 130px;
    }
    .metric-value { font-size: 36px; font-weight: bold; color: #667eea; }
    .metric-label { font-size: 12px; color: #666; text-transform: uppercase; margin-top: 5px; }
    .divider-thick { border-top: 3px solid #667eea; margin: 40px 0; }
</style>
""", unsafe_allow_html=True)

# TITRE PRINCIPAL
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
    
    # ===== SEPARATOR LES SECTIONS =====
    col_n = 'N°' if 'N°' in df.columns else df.columns[0]
    
    df_a = df[df[col_n].astype(str).str.strip().apply(lambda x: x.isdigit() and 1 <= int(x) <= 10)]
    df_b = df[df[col_n].astype(str).str.contains('B', na=False)]
    df_c = df[df[col_n].astype(str).str.contains('C', na=False)]
    
    # Fonction pour créer une section
    def create_section(section_df, title, color_class, color_hex):
        st.markdown(f"<h2 class='{color_class}'>{title}</h2>", unsafe_allow_html=True)
        
        # METRIQUES
        total_livres = len(section_df[section_df['Total'] > 0])
        total_objectifs = len(section_df)
        taux = (total_livres / total_objectifs * 100) if total_objectifs > 0 else 0
        total_real = int(section_df[mois].sum().sum())
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🎯 Objectifs", total_objectifs)
        with col2:
            st.metric("✅ Realises", total_livres)
        with col3:
            st.metric("📈 Taux %", f"{taux:.1f}%")
        with col4:
            st.metric("🔄 Actions", total_real)
        
        # GRAPHIQUE COURBES
        col1, col2 = st.columns(2)
        
        with col1:
            mois_values = [section_df[m].sum() for m in mois]
            mois_cumul = []
            cumul = 0
            for val in mois_values:
                cumul += val
                mois_cumul.append(cumul)
            
            fig_curve = go.Figure()
            
            fig_curve.add_trace(go.Scatter(
                x=mois,
                y=mois_values,
                mode='lines+markers',
                name='Realisations Mensuelles',
                line=dict(color=color_hex, width=4),
                marker=dict(size=12, color=color_hex),
                fill='tozeroy',
                fillcolor=f'rgba({color_hex[1:3]}, {color_hex[3:5]}, {color_hex[5:7]}, 0.2)',
                hovertemplate='<b>%{x}</b><br>Realisations: %{y}<extra></extra>'
            ))
            
            fig_curve.add_trace(go.Scatter(
                x=mois,
                y=mois_cumul,
                mode='lines+markers',
                name='Cumul',
                line=dict(color='#f5576c', width=3, dash='dash'),
                marker=dict(size=8, color='#f5576c'),
                hovertemplate='<b>%{x}</b><br>Cumul: %{y}<extra></extra>'
            ))
            
            fig_curve.update_layout(
                title="<b>Evolution Mensuelle</b>",
                xaxis_title="Mois",
                yaxis_title="Realisations",
                height=400,
                template='plotly_white',
                hovermode='x unified',
                font=dict(size=11),
                plot_bgcolor='rgba(240,240,240,0.5)'
            )
            
            st.plotly_chart(fig_curve, use_container_width=True)
        
        with col2:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=taux,
                title={'text': "<b>Taux Realisation</b>"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': color_hex},
                    'steps': [
                        {'range': [0, 33], 'color': "#ffcccc"},
                        {'range': [33, 66], 'color': "#ffffcc"},
                        {'range': [66, 100], 'color': "#ccffcc"}
                    ]
                }
            ))
            fig_gauge.update_layout(height=400, font=dict(size=12))
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        # HEATMAP
        st.markdown("#### 🔥 Progression Detaillee par Livrable")
        
        livrable_col = 'Livrable' if 'Livrable' in section_df.columns else section_df.columns[1]
        df_heatmap = section_df[[livrable_col] + mois].head(10)
        
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=df_heatmap[mois].values,
            x=mois,
            y=df_heatmap[livrable_col].values,
            colorscale='RdYlGn',
            colorbar=dict(title="Realise"),
            hovertemplate='<b>%{y}</b><br>%{x}: %{z}<extra></extra>'
        ))
        
        fig_heatmap.update_layout(
            title="<b>Heatmap - Realisation par Livrable</b>",
            xaxis_title="Mois",
            yaxis_title="Livrables",
            height=350,
            font=dict(size=10)
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # TABLEAU SYNTHESE
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Top Livrables")
            top_livs = section_df.nlargest(5, 'Total')
            
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                x=top_livs['Total'],
                y=top_livs[livrable_col],
                orientation='h',
                marker=dict(color=color_hex),
                text=top_livs['Total'],
                textposition='auto',
                hovertemplate='<b>%{y}</b><br>Realise: %{x}<extra></extra>'
            ))
            fig_bar.update_layout(
                title="<b>Top 5 Livrables</b>",
                xaxis_title="Nombre",
                height=350,
                template='plotly_white',
                showlegend=False
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            st.markdown("#### 📋 Resume Mensuel")
            resume = pd.DataFrame({
                'Mois': mois,
                'Realise': mois_values,
                'Cumul': mois_cumul
            })
            st.dataframe(resume, use_container_width=True, hide_index=True)
        
        st.markdown("<div class='divider-thick'></div>", unsafe_allow_html=True)
    
    # ===== SECTION A : PRIORITAIRES =====
    if len(df_a) > 0:
        create_section(df_a, "A. 🎯 ACTIVITES PRIORITAIRES", "section-a", "#667eea")
    
    # ===== SECTION B : GOUVERNANCE =====
    if len(df_b) > 0:
        create_section(df_b, "B. 📋 ACTIVITES DE GOUVERNANCE", "section-b", "#f5576c")
    
    # ===== SECTION C : SUPERVISEUR =====
    if len(df_c) > 0:
        create_section(df_c, "C. 👁️ AXES SUPERVISEUR", "section-c", "#00f2fe")
    
    # SYNTHESE FINALE
    st.markdown("<h2 style='text-align: center; color: #1a1a2e; margin-top: 50px;'>📊 SYNTHESE GLOBALE</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_global_objectifs = len(df)
    total_global_realises = len(df[df['Total'] > 0])
    taux_global = (total_global_realises / total_global_objectifs * 100) if total_global_objectifs > 0 else 0
    total_global_actions = int(df[mois].sum().sum())
    
    with col1:
        st.metric("🎯 Objectifs Totaux", total_global_objectifs)
    with col2:
        st.metric("✅ Realises Totaux",

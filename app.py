import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import time

st.set_page_config(page_title="DSVCo Dashboard S1 2026", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    h1 { text-align: center; color: #1a1a2e; font-size: 48px; margin-bottom: 5px; font-weight: bold; }
    h2 { text-align: center; color: #16213e; font-size: 24px; margin-top: 30px; }
    .subtitle { text-align: center; color: #667eea; font-size: 18px; font-weight: 600; margin-bottom: 30px; }
    .metric-container {
        display: flex;
        gap: 15px;
        margin-bottom: 30px;
        justify-content: center;
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        min-width: 180px;
        border-left: 5px solid #667eea;
    }
    .metric-value { font-size: 42px; font-weight: bold; color: #667eea; }
    .metric-label { font-size: 13px; color: #666; text-transform: uppercase; margin-top: 5px; }
</style>
""", unsafe_allow_html=True)

# TITRE
st.markdown("<h1>📊 TABLEAU DE BORD DSVCo S1 2026</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Direction de la Sante et de la Vaccination Communautaire<br>Suivi EN TEMPS REEL - Janvier a Juin 2026</p>", unsafe_allow_html=True)

sheet_url = "https://docs.google.com/spreadsheets/d/1BVEEDaDQZ9cauGKau03BFc7rvmUoOX8aiUDOHQTqyV0/edit?usp=sharing"

try:
    sheet_id = sheet_url.split('/d/')[1].split('/')[0]
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
    
    df = pd.read_csv(csv_url)
    
    st.success("✅ Connecte a Google Sheets - EN TEMPS REEL")
    
    # Corriger les noms de colonnes avec accents
    mois = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin']
    
    # Convertir en numérique
    for mois_col in mois:
        if mois_col in df.columns:
            df[mois_col] = pd.to_numeric(df[mois_col], errors='coerce').fillna(0)
    
    df['Total'] = df[mois].sum(axis=1)
    
    # METRIQUES GLOBALES
    total_livres = len(df[df['Total'] > 0])
    total_objectifs = len(df)
    taux_global = (total_livres / total_objectifs * 100) if total_objectifs > 0 else 0
    total_realisations = int(df[mois].sum().sum())
    
    # Afficher les métriques en haut
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎯 Objectifs", total_objectifs, "livrables")
    with col2:
        st.metric("✅ Realises", total_livres, "completes")
    with col3:
        st.metric("📈 Taux Global", f"{taux_global:.1f}%", "+10%")
    with col4:
        st.metric("🔄 Realisations", total_realisations, "actions")
    
    st.divider()
    
    # ===== GRAND GRAPHIQUE : COURBES DE PROGRESSION =====
    st.markdown("<h2>📈 Evolution Globale par Mois</h2>", unsafe_allow_html=True)
    
    mois_values = [df[m].sum() for m in mois]
    mois_cumul = []
    cumul = 0
    for val in mois_values:
        cumul += val
        mois_cumul.append(cumul)
    
    fig_evolution = go.Figure()
    
    # Courbe réalisations mensuelles
    fig_evolution.add_trace(go.Scatter(
        x=mois,
        y=mois_values,
        mode='lines+markers',
        name='Realisations Mensuelles',
        line=dict(color='#667eea', width=4),
        marker=dict(size=12, color='#667eea', line=dict(color='white', width=2)),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.2)',
        hovertemplate='<b>%{x}</b><br>Realisations: %{y}<extra></extra>'
    ))
    
    # Courbe cumulative
    fig_evolution.add_trace(go.Scatter(
        x=mois,
        y=mois_cumul,
        mode='lines+markers',
        name='Cumul Progressif',
        line=dict(color='#f5576c', width=4, dash='dash'),
        marker=dict(size=10, color='#f5576c'),
        hovertemplate='<b>%{x}</b><br>Cumul: %{y}<extra></extra>'
    ))
    
    fig_evolution.update_layout(
        title="<b>Evolution Mensuelle et Cumulative des Realisations</b>",
        xaxis_title="Mois",
        yaxis_title="Nombre de Realisations",
        height=500,
        template='plotly_white',
        hovermode='x unified',
        font=dict(size=12),
        legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0.8)'),
        plot_bgcolor='rgba(240,240,240,0.5)'
    )
    
    st.plotly_chart(fig_evolution, use_container_width=True)
    
    # ===== HEATMAP : PROGRESSION PAR LIVRABLE =====
    st.markdown("<h2>🔥 Heatmap - Progression par Livrable</h2>", unsafe_allow_html=True)
    
    df_heatmap = df[['Livrable'] + mois].head(10)
    
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=df_heatmap[mois].values,
        x=mois,
        y=df_heatmap['Livrable'].values,
        colorscale='RdYlGn',
        colorbar=dict(title="Realisations"),
        hovertemplate='<b>%{y}</b><br>%{x}: %{z}<extra></extra>'
    ))
    
    fig_heatmap.update_layout(
        title="<b>Progression Detaillee par Livrable</b>",
        xaxis_title="Mois",
        yaxis_title="Livrables",
        height=400,
        font=dict(size=11)
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # ===== GRAPHIQUES CÔTE À CÔTE =====
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Distribution des Realisations")
        top_livs = df.nlargest(10, 'Total')
        livrable_col = 'Livrable' if 'Livrable' in df.columns else df.columns[1]
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=top_livs['Total'],
            y=top_livs[livrable_col],
            orientation='h',
            marker=dict(
                color=top_livs['Total'],
                colorscale='Viridis',
                line=dict(color='darkblue', width=1)
            ),
            text=top_livs['Total'],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Realise: %{x}<extra></extra>'
        ))
        fig_bar.update_layout(
            title="<b>Top 10 Livrables Realises</b>",
            xaxis_title="Nombre",
            height=400,
            template='plotly_white',
            showlegend=False,
            font=dict(size=11)
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.markdown("#### 🎯 Taux de Realisation Global")
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=taux_global,
            title={'text': "Taux Global (%)"},
            delta={'reference': 50, 'suffix': "%"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#667eea", 'thickness': 0.7},
                'steps': [
                    {'range': [0, 25], 'color': "#ffebee"},
                    {'range': [25, 50], 'color': "#fff3e0"},
                    {'range': [50, 75], 'color': "#f1f8e9"},
                    {'range': [75, 100], 'color': "#e8f5e9"}
                ],
                'threshold': {
                    'line': {'color': "#667eea", 'width': 4},
                    'thickness': 0.75,
                    'value': 75
                }
            }
        ))
        fig_gauge.update_layout(height=400, font=dict(size=12))
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    # ===== SECTION FINALE : SYNTHÈSE =====
    st.divider()
    st.markdown("<h2>📋 Synthese Detaillee</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sections = ['A. Prioritaires', 'B. Gouvernance', 'C. Superviseur']
        if 'N°' in df.columns:
            col_n = 'N°'
            df_a = df[df[col_n].astype(str).str.strip().apply(lambda x: x.isdigit() and 1 <= int(x) <= 10)]
            score_a = (len(df_a[df_a['Total'] > 0]) / len(df_a) * 100) if len(df_a) > 0 else 0
            
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=[score_a, 60, 50],
                theta=sections,
                fill='toself',
                name='Realisation (%)',
                line=dict(color='#667eea', width=2),
                fillcolor='rgba(102, 126, 234, 0.3)'
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                title="<b>Realisation par Section</b>",
                height=400,
                font=dict(size=11)
            )
            st.plotly_chart(fig_radar, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Tableau Resume")
        resume = pd.DataFrame({
            'Mois': mois,
            'Realisations': mois_values,
            'Cumul': mois_cumul,
            'Taux %': [round((mois_cumul[i] / total_realisations * 100), 1) if total_realisations > 0 else 0 for i in range(len(mois))]
        })
        st.dataframe(resume, use_container_width=True, hide_index=True)
    
    with col3:
        st.markdown("#### 🎯 Indicateurs Cles")
        indicateurs = f"""
        **Objectifs Totaux:** {total_objectifs}  
        **Realises:** {total_livres}  
        **Taux Realisation:** {taux_global:.1f}%  
        **Total Actions:** {total_realisations}  
        **Moyenne/Mois:** {total_realisations/6:.1f}
        """
        st.markdown(indicateurs)
    
    # Footer
    st.divider()
    st.markdown(f"<p style='text-align: center; color: #999; font-size: 11px;'>Dashboard DSVCo S1 2026 - Donnees en temps reel<br>Derniere mise a jour: {datetime.now().strftime('%d/%m/%Y a %H:%M:%S')}</p>", unsafe_allow_html=True)
    
    # Auto-refresh
    time.sleep(30)
    st.rerun()

except Exception as e:
    st.error(f"Erreur: {str(e)}")
    st.info("Verifiez que le Google Sheet est partage publiquement")

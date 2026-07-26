import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

st.set_page_config(
    page_title="DSVCo Dashboard S1 2026",
    layout="wide",
    initial_sidebar_state="collapsed"  # Masquer la sidebar
)

# CSS pour un look professionnel
st.markdown("""
<style>
    /* Masquer les éléments techniques */
    .stTextInput { display: none; }
    .stCheckbox { display: none; }
    .stButton { display: none; }
    
    /* Styling des métriques */
    .main-metric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        margin: 10px;
    }
    .metric-value {
        font-size: 56px;
        font-weight: bold;
        margin: 15px 0;
        letter-spacing: 2px;
    }
    .metric-label {
        font-size: 16px;
        opacity: 0.95;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* En-têtes */
    h1 { text-align: center; color: #333; font-size: 42px; margin-bottom: 10px; }
    h2 { text-align: center; color: #667eea; font-size: 28px; margin-top: 40px; margin-bottom: 30px; }
    
    /* Fond */
    .stApp { background: linear-gradient(to bottom, #f8f9fa, #ffffff); }
</style>
""", unsafe_allow_html=True)

# LIEN HARDCODÉ (pas besoin de sidebar)
sheet_url = "https://docs.google.com/spreadsheets/d/1ShEd0ZsaqX81Qz7iit/edit?usp=sharing"

try:
    # Extraire l'ID et charger les données
    sheet_id = sheet_url.split('/d/')[1].split('/')[0]
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
    
    df = pd.read_csv(csv_url)
    
    # NETTOYAGE DES DONNÉES
    mois = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin']
    for mois_col in mois:
        if mois_col in df.columns:
            df[mois_col] = pd.to_numeric(df[mois_col], errors='coerce').fillna(0)
    
    df['Total'] = df[mois].sum(axis=1)
    
    # CALCUL DES MÉTRIQUES
    total_livres = len(df[df['Total'] > 0]) if 'Total' in df.columns else 0
    total_objectifs = len(df)
    taux_global = (total_livres / total_objectifs * 100) if total_objectifs > 0 else 0
    total_realisations = int(df[mois].sum().sum()) if any(m in df.columns for m in mois) else 0
    
    # ===== TITRE =====
    st.markdown("""
    <h1>📊 TABLEAU DE BORD DSVCo S1 2026</h1>
    <p style="text-align: center; font-size: 18px; color: #666; margin-bottom: 30px;">
        Direction de la Santé et de la Vaccination Communautaire<br>
        <span style="color: #667eea; font-weight: bold;">Suivi EN TEMPS RÉEL - Janvier à Juin 2026</span>
    </p>
    """, unsafe_allow_html=True)
    
    # ===== INDICATEURS CLÉS =====
    st.markdown("<h2>📈 INDICATEURS CLÉS</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4, gap="large")
    
    with col1:
        st.markdown(f"""
        <div class="main-metric" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <div class="metric-label">🎯 Objectifs</div>
            <div class="metric-value">{total_objectifs}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="main-metric" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <div class="metric-label">✅ Réalisés</div>
            <div class="metric-value">{total_livres}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="main-metric" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <div class="metric-label">📊 Taux</div>
            <div class="metric-value">{taux_global:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="main-metric" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <div class="metric-label">📈 Réalisations</div>
            <div class="metric-value">{total_realisations}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ===== GRAPHIQUES =====
    st.markdown("<h2>📊 ANALYSES DÉTAILLÉES</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    # Graphique 1 : Progression mensuelle
    with col1:
        mois_values = []
        for m in mois:
            if m in df.columns:
                mois_values.append(df[m].sum())
            else:
                mois_values.append(0)
        
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=mois,
            y=mois_values,
            marker=dict(
                color=mois_values,
                colorscale='Viridis',
                line=dict(color='darkblue', width=2),
                showscale=False
            ),
            text=mois_values,
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Réalisations: %{y}<extra></extra>',
            showlegend=False
        ))
        fig1.update_layout(
            title="<b>Progression Mensuelle</b>",
            xaxis_title="Mois",
            yaxis_title="Nombre de réalisations",
            height=450,
            template='plotly_white',
            font=dict(size=12),
            margin=dict(t=50, b=50, l=50, r=50)
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    # Graphique 2 : Top livrables
    with col2:
        top_livs = df.nlargest(10, 'Total')
        
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            y=top_livs['Livrable'] if 'Livrable' in top_livs.columns else top_livs.iloc[:, 1],
            x=top_livs['Total'],
            orientation='h',
            marker=dict(
                color=top_livs['Total'],
                colorscale='Reds',
                line=dict(color='darkred', width=2),
                showscale=False
            ),
            text=top_livs['Total'],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Réalisé: %{x}<extra></extra>',
            showlegend=False
        ))
        fig2.update_layout(
            title="<b>Top 10 Livrables</b>",
            xaxis_title="Réalisations",
            height=450,
            template='plotly_white',
            font=dict(size=12),
            margin=dict(t=50, b=50, l=50, r=50)
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Graphique 3 : Jauge + Radar
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        fig3 = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=taux_global,
            title={'text': "<b>Taux Réalisation Global</b>"},
            delta={'reference': 50, 'suffix': "%"},
            gauge={
                'axis': {'range': [0, 100], 'tickfont': {'size': 12}},
                'bar': {'color': "#667eea", 'thickness': 0.7},
                'steps': [
                    {'range': [0, 33], 'color': "#ffcccc"},
                    {'range': [33, 66], 'color': "#ffffcc"},
                    {'range': [66, 100], 'color': "#ccffcc"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig3.update_layout(height=450, font=dict(size=12))
        st.plotly_chart(fig3, use_container_width=True)
    
    # Graphique 4 : Radar
    with col2:
        sections = []
        scores = []
        
        if 'N°' in df.columns:
            # Section A (1-10)
            df_a = df[df['N°'].astype(str).str.strip().apply(lambda x: x.isdigit() and 1 <= int(x) <= 10)]
            if len(df_a) > 0:
                sections.append("A. Prioritaires")
                scores.append((len(df_a[df_a['Total'] > 0]) / len(df_a) * 100))
            
            # Section B (B1-B5)
            df_b = df[df['N°'].astype(str).str.contains('B', na=False)]
            if len(df_b) > 0:
                sections.append("B. Gouvernance")
                scores.append((len(df_b[df_b['Total'] > 0]) / len(df_b) * 100))
            
            # Section C (C1-C5)
            df_c = df[df['N°'].astype(str).str.contains('C', na=False)]
            if len(df_c) > 0:
                sections.append("C. Superviseur")
                scores.append((len(df_c[df_c['Total'] > 0]) / len(df_c) * 100))
        
        if sections:
            fig4 = go.Figure()
            fig4.add_trace(go.Scatterpolar(
                r=scores,
                theta=sections,
                fill='toself',
                name='Réalisation (%)',
                line=dict(color='#667eea', width=2),
                fillcolor='rgba(102, 126, 234, 0.3)',
                hovertemplate='<b>%{theta}</b><br>%{r:.1f}%<extra></extra>'
            ))
            fig4.update_layout(
                title="<b>Réalisation par Section</b>",
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100],
                        tickfont=dict(size=11)
                    ),
                    angularaxis=dict(tickfont=dict(size=12))
                ),
                height=450,
                template='plotly_white',
                font=dict(size=12),
                showlegend=True
            )
            st.plotly_chart(fig4, use_container_width=True)
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #999; font-size: 12px; margin-top: 30px;">
        <p>Dashboard DSVCo S1 2026 • Mise à jour en temps réel</p>
        # À la place de:
st.markdown("""
<div style="text-align: center; color: #999; font-size: 12px; margin-top: 30px;">
    <p>Dashboard DSVCo S1 2026 • Mise à jour en temps réel</p>
    <p>Dernière mise à jour: """ + datetime.now().strftime("%d/%m/%Y à %H:%M:%S") + """</p>
</div>
""", unsafe_allow_html=True)

# Remplacer par:
st.markdown(
    f"""<div style="text-align: center; color: #999; font-size: 12px; margin-top: 30px;">
    <p>Dashboard DSVCo S1 2026 • Mise à jour en temps réel</p>
    <p>Dernière mise à jour: {datetime.now().strftime("%d/%m/%Y à %H:%M:%S")}</p>
</div>""",
    unsafe_allow_html=True
)

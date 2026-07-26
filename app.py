import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

st.set_page_config(page_title="DSVCo Dashboard S1 2026", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .main-metric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        margin: 10px;
    }
    .metric-value { font-size: 56px; font-weight: bold; margin: 15px 0; }
    .metric-label { font-size: 16px; opacity: 0.95; text-transform: uppercase; }
    h1 { text-align: center; color: #333; font-size: 42px; }
    h2 { text-align: center; color: #667eea; font-size: 28px; margin-top: 40px; }
    .stApp { background: linear-gradient(to bottom, #f8f9fa, #ffffff); }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>TABLEAU DE BORD DSVCo S1 2026</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color: #666;'>Direction de la Sante et de la Vaccination Communautaire<br><span style='color: #667eea; font-weight: bold;'>Suivi EN TEMPS REEL - Janvier a Juin 2026</span></p>", unsafe_allow_html=True)

# LIEN GOOGLE SHEET CORRECT
sheet_url = "https://docs.google.com/spreadsheets/d/1BVEEDaDQZ9cauGKau03BFc7rvmUoOX8aiUDOHQTqyV0/edit?usp=sharing"

try:
    sheet_id = sheet_url.split('/d/')[1].split('/')[0]
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
    
    df = pd.read_csv(csv_url)
    
    st.success("Connecte a Google Sheets - EN TEMPS REEL")
    
    # Nettoyer les donnees
    mois = ['Jan', 'Fev', 'Mar', 'Avr', 'Mai', 'Juin']
    
    for mois_col in mois:
        if mois_col in df.columns:
            df[mois_col] = pd.to_numeric(df[mois_col], errors='coerce').fillna(0)
    
    df['Total'] = df[mois].sum(axis=1)
    
    # METRIQUES
    total_livres = len(df[df['Total'] > 0]) if 'Total' in df.columns else 0
    total_objectifs = len(df)
    taux_global = (total_livres / total_objectifs * 100) if total_objectifs > 0 else 0
    total_realisations = int(df[mois].sum().sum()) if any(m in df.columns for m in mois) else 0
    
    # INDICATEURS CLES
    st.markdown("<h2>INDICATEURS CLES</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4, gap="large")
    
    with col1:
        st.markdown(f"""
        <div class="main-metric" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <div class="metric-label">Objectifs</div>
            <div class="metric-value">{total_objectifs}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="main-metric" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <div class="metric-label">Realises</div>
            <div class="metric-value">{total_livres}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="main-metric" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <div class="metric-label">Taux</div>
            <div class="metric-value">{taux_global:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="main-metric" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <div class="metric-label">Realisations</div>
            <div class="metric-value">{total_realisations}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # GRAPHIQUES
    st.markdown("<h2>ANALYSES DETAILLEES</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        mois_values = [df[m].sum() if m in df.columns else 0 for m in mois]
        
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=mois,
            y=mois_values,
            marker=dict(color=mois_values, colorscale='Viridis', line=dict(color='darkblue', width=2)),
            text=mois_values,
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Realisations: %{y}<extra></extra>'
        ))
        fig1.update_layout(
            title="<b>Progression Mensuelle</b>",
            xaxis_title="Mois",
            yaxis_title="Realisations",
            height=450,
            template='plotly_white',
            font=dict(size=12)
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        top_livs = df.nlargest(10, 'Total')
        livrable_col = 'Livrable' if 'Livrable' in df.columns else df.columns[1]
        
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            y=top_livs[livrable_col],
            x=top_livs['Total'],
            orientation='h',
            marker=dict(color=top_livs['Total'], colorscale='Reds', line=dict(color='darkred', width=2)),
            text=top_livs['Total'],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Realise: %{x}<extra></extra>'
        ))
        fig2.update_layout(
            title="<b>Top 10 Livrables</b>",
            xaxis_title="Realisations",
            height=450,
            template='plotly_white',
            font=dict(size=12)
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        fig3 = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=taux_global,
            title={'text': "<b>Taux Realisation Global</b>"},
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
        fig3.update_layout(height=450, font=dict(size=12))
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        sections = []
        scores = []
        
        if 'N' in df.columns or df.columns[0] in ['N', 'N°']:
            col_n = 'N' if 'N' in df.columns else df.columns[0]
            
            df_a = df[df[col_n].astype(str).str.strip().apply(lambda x: x.isdigit() and 1 <= int(x) <= 10)]
            if len(df_a) > 0:
                sections.append("A. Prioritaires")
                scores.append((len(df_a[df_a['Total'] > 0]) / len(df_a) * 100))
            
            df_b = df[df[col_n].astype(str).str.contains('B', na=False)]
            if len(df_b) > 0:
                sections.append("B. Gouvernance")
                scores.append((len(df_b[df_b['Total'] > 0]) / len(df_b) * 100))
            
            df_c = df[df[col_n].astype(str).str.contains('C', na=False)]
            if len(df_c) > 0:
                sections.append("C. Superviseur")
                scores.append((len(df_c[df_c['Total'] > 0]) / len(df_c) * 100))
        
        if sections:
            fig4 = go.Figure()
            fig4.add_trace(go.Scatterpolar(
                r=scores,
                theta=sections,
                fill='toself',
                name='Realisation (%)',
                line=dict(color='#667eea', width=2),
                fillcolor='rgba(102, 126, 234, 0.3)',
                hovertemplate='<b>%{theta}</b><br>%{r:.1f}%<extra></extra>'
            ))
            fig4.update_layout(
                title="<b>Realisation par Section</b>",
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                height=450,
                template='plotly_white',
                font=dict(size=12)
            )
            st.plotly_chart(fig4, use_container_width=True)
    
    # TABLEAU DETAIL
    st.divider()
    st.markdown("<h2>DONNEES DETAILLEES</h2>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Footer
    st.divider()
    st.markdown(f"<p style='text-align: center; color: #999; font-size: 12px;'>Dashboard DSVCo S1 2026 - Suivi en temps reel<br>Derniere mise a jour: {datetime.now().strftime('%d/%m/%Y a %H:%M:%S')}</p>", unsafe_allow_html=True)
    
    # Auto-refresh
    time.sleep(30)
    st.rerun()

except Exception as e:
    st.error(f"Erreur de chargement: {str(e)}")
    st.info("Le Google Sheet est peut-etre inaccessible. Verifiez qu'il est partage publiquement.")

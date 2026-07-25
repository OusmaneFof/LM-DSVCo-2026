import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import time
from datetime import datetime

st.set_page_config(page_title="DSVCo Dashboard S1 2026", layout="wide", initial_sidebar_state="expanded")

# CSS
st.markdown("""
<style>
    .main-metric { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 15px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
    .metric-value { font-size: 48px; font-weight: bold; margin: 10px 0; }
    .metric-label { font-size: 14px; opacity: 0.9; }
    .status-green { background: #C8E6C9; }
    .status-orange { background: #FFE0B2; }
    .status-red { background: #FFCDD2; }
    .section-card { border-left: 5px solid #667eea; padding: 15px; margin: 15px 0; background: #f8f9fa; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

st.title("📊 TABLEAU DE BORD DSVCo S1 2026")
st.markdown("**Direction de la Santé et de la Vaccination Communautaire**")

# SIDEBAR
with st.sidebar:
    st.header("⚙️ CONFIGURATION")
    
    sheet_url = st.text_input(
        "📊 Lien Google Sheet",
        placeholder="https://docs.google.com/spreadsheets/d/..."
    )
    
    auto_refresh = st.checkbox("🔄 Auto-refresh (30 sec)", value=True)
    
    if st.button("🔄 Rafraîchir"):
        st.rerun()
    
    st.divider()
    st.markdown("**📅 PÉRIODE : JANVIER - JUIN 2026**")
    st.metric("⏰ Mise à jour", datetime.now().strftime("%H:%M:%S"))

if sheet_url:
    try:
        # Charger les données
        sheet_id = sheet_url.split('/d/')[1].split('/')[0]
        
        # Sheet 1 : Activités prioritaires (gid=0)
        csv_url_1 = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
        df_prioritaires = pd.read_csv(csv_url_1)
        
        # Sheet 2 : Gouvernance (gid=1)
        csv_url_2 = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=1"
        df_gouvernance = pd.read_csv(csv_url_2)
        
        # Sheet 3 : Axes superviseur (gid=2)
        csv_url_3 = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=2"
        df_axes = pd.read_csv(csv_url_3)
        
        st.success("✅ Connecté à Google Sheets - EN TEMPS RÉEL")
        
        # CALCULER LES MÉTRIQUES
        def calculate_completion(df, value_cols=['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin']):
            """Calculer le taux de réalisation"""
            total = 0
            count = 0
            for col in value_cols:
                if col in df.columns:
                    values = pd.to_numeric(df[col], errors='coerce').fillna(0)
                    total += values.sum()
                    count += len(values)
            return (total / count * 100) if count > 0 else 0
        
        comp_prioritaires = calculate_completion(df_prioritaires)
        comp_gouvernance = calculate_completion(df_gouvernance)
        comp_axes = calculate_completion(df_axes)
        comp_global = (comp_prioritaires + comp_gouvernance + comp_axes) / 3
        
        # ===== VISUEL PRINCIPAL =====
        st.markdown("# 📈 INDICATEURS GLOBAUX")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="main-metric">
                <div class="metric-label">🎯 TAUX GLOBAL</div>
                <div class="metric-value">{comp_global:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="main-metric" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <div class="metric-label">A. PRIORITAIRES</div>
                <div class="metric-value">{comp_prioritaires:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="main-metric" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <div class="metric-label">B. GOUVERNANCE</div>
                <div class="metric-value">{comp_gouvernance:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="main-metric" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                <div class="metric-label">C. SUPERVISEUR</div>
                <div class="metric-value">{comp_axes:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        # ===== SECTION A =====
        st.markdown("## A. 🎯 ACTIVITÉS PRIORITAIRES")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Graphique progression A
            mois = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin']
            values_a = [df_prioritaires[m].sum() if m in df_prioritaires.columns else 0 for m in mois]
            
            fig_a = go.Figure()
            fig_a.add_trace(go.Bar(
                x=mois,
                y=values_a,
                marker=dict(color='#f5576c', line=dict(color='darkred', width=2)),
                text=values_a,
                textposition='auto',
                hovertemplate='<b>%{x}</b><br>Réalisé: %{y}<extra></extra>'
            ))
            fig_a.update_layout(
                title="📊 Progression Mensuelle Section A",
                height=350,
                template='plotly_white'
            )
            st.plotly_chart(fig_a, use_container_width=True)
        
        with col2:
            # Jauge A
            fig_gauge_a = go.Figure(go.Indicator(
                mode="gauge+number",
                value=comp_prioritaires,
                title={'text': "Taux Réalisation A"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#f5576c"},
                    'steps': [
                        {'range': [0, 33], 'color': "#ffcccc"},
                        {'range': [33, 66], 'color': "#ffffcc"},
                        {'range': [66, 100], 'color': "#ccffcc"}
                    ]
                }
            ))
            fig_gauge_a.update_layout(height=350)
            st.plotly_chart(fig_gauge_a, use_container_width=True)
        
        # Tableau A
        st.dataframe(df_prioritaires, use_container_width=True, hide_index=True)
        
        st.divider()
        
        # ===== SECTION B =====
        st.markdown("## B. 📋 ACTIVITÉS DE GOUVERNANCE")
        
        col1, col2 = st.columns(2)
        
        with col1:
            mois = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin']
            values_b = [df_gouvernance[m].sum() if m in df_gouvernance.columns else 0 for m in mois]
            
            fig_b = go.Figure()
            fig_b.add_trace(go.Bar(
                x=mois,
                y=values_b,
                marker=dict(color='#00f2fe', line=dict(color='darkblue', width=2)),
                text=values_b,
                textposition='auto'
            ))
            fig_b.update_layout(
                title="📊 Progression Mensuelle Section B",
                height=350,
                template='plotly_white'
            )
            st.plotly_chart(fig_b, use_container_width=True)
        
        with col2:
            fig_gauge_b = go.Figure(go.Indicator(
                mode="gauge+number",
                value=comp_gouvernance,
                title={'text': "Taux Réalisation B"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#00f2fe"},
                    'steps': [
                        {'range': [0, 33], 'color': "#ccf0ff"},
                        {'range': [33, 66], 'color': "#ffffcc"},
                        {'range': [66, 100], 'color': "#ccffcc"}
                    ]
                }
            ))
            fig_gauge_b.update_layout(height=350)
            st.plotly_chart(fig_gauge_b, use_container_width=True)
        
        st.dataframe(df_gouvernance, use_container_width=True, hide_index=True)
        
        st.divider()
        
        # ===== SECTION C =====
        st.markdown("## C. 🎯 AXES SPÉCIFIQUES - RÔLE DE SUPERVISEUR")
        
        col1, col2 = st.columns(2)
        
        with col1:
            mois = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin']
            values_c = [df_axes[m].sum() if m in df_axes.columns else 0 for m in mois]
            
            fig_c = go.Figure()
            fig_c.add_trace(go.Bar(
                x=mois,
                y=values_c,
                marker=dict(color='#43e97b', line=dict(color='darkgreen', width=2)),
                text=values_c,
                textposition='auto'
            ))
            fig_c.update_layout(
                title="📊 Progression Mensuelle Section C",
                height=350,
                template='plotly_white'
            )
            st.plotly_chart(fig_c, use_container_width=True)
        
        with col2:
            fig_gauge_c = go.Figure(go.Indicator(
                mode="gauge+number",
                value=comp_axes,
                title={'text': "Taux Réalisation C"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#43e97b"},
                    'steps': [
                        {'range': [0, 33], 'color': "#ffcccc"},
                        {'range': [33, 66], 'color': "#ffffcc"},
                        {'range': [66, 100], 'color': "#ccffcc"}
                    ]
                }
            ))
            fig_gauge_c.update_layout(height=350)
            st.plotly_chart(fig_gauge_c, use_container_width=True)
        
        st.dataframe(df_axes, use_container_width=True, hide_index=True)
        
        # ===== SYNTHÈSE GLOBALE =====
        st.divider()
        st.markdown("## 📊 SYNTHÈSE GLOBALE")
        
        # Radar chart
        sections = ['A. Prioritaires', 'B. Gouvernance', 'C. Superviseur']
        scores = [comp_prioritaires, comp_gouvernance, comp_axes]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=scores,
            theta=sections,
            fill='toself',
            name='Taux de réalisation',
            line=dict(color='#667eea'),
            fillcolor='rgba(102, 126, 234, 0.3)'
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            ),
            height=400,
            template='plotly_white'
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Auto-refresh
        if auto_refresh:
            st.info("🔄 Auto-refresh activé - Mise à jour toutes les 30 secondes")
            time.sleep(30)
            st.rerun()
        
    except Exception as e:
        st.error(f"❌ Erreur : {str(e)}")
        st.info("Vérifiez que le lien est complet et le sheet partagé")

else:
    st.info("👈 Entrez le lien de votre Google Sheet pour voir le dashboard")

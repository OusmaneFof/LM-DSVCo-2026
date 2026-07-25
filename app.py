import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

st.set_page_config(page_title="DSVCo Dashboard S1 2026", layout="wide")

st.markdown("""
<style>
    .main-metric { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 15px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
    .metric-value { font-size: 48px; font-weight: bold; margin: 10px 0; }
    .metric-label { font-size: 14px; opacity: 0.9; }
</style>
""", unsafe_allow_html=True)

st.title("📊 TABLEAU DE BORD DSVCo S1 2026")
st.markdown("**Direction de la Santé et de la Vaccination Communautaire**")

with st.sidebar:
    st.header("⚙️ CONFIGURATION")
    
    sheet_url = st.text_input(
        "📊 Lien Google Sheet",
        value="https://docs.google.com/spreadsheets/d/1ShEd0ZsaqX81Qz7iit/edit?usp=sharing"
    )
    
    auto_refresh = st.checkbox("🔄 Auto-refresh (30 sec)", value=True)
    
    if st.button("🔄 Rafraîchir"):
        st.rerun()
    
    st.metric("⏰ Mise à jour", datetime.now().strftime("%H:%M:%S"))

if sheet_url:
    try:
        # Extraire l'ID
        sheet_id = sheet_url.split('/d/')[1].split('/')[0]
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
        
        # Charger les données
        df = pd.read_csv(csv_url)
        
        st.success("✅ Connecté à Google Sheets - EN TEMPS RÉEL")
        
        # NETTOYAGE DES DONNÉES
        # Convertir les colonnes de mois en numérique
        mois = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin']
        for mois_col in mois:
            if mois_col in df.columns:
                df[mois_col] = pd.to_numeric(df[mois_col], errors='coerce').fillna(0)
        
        # Calculer les totaux
        df['Total'] = df[mois].sum(axis=1)
        
        # SECTION 1 : MÉTRIQUES CLÉS
        st.markdown("## 📈 INDICATEURS CLÉS")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_livres = len(df[df['Total'] > 0]) if 'Total' in df.columns else 0
        total_objectifs = len(df)
        taux_global = (total_livres / total_objectifs * 100) if total_objectifs > 0 else 0
        total_realisations = df[mois].sum().sum() if any(m in df.columns for m in mois) else 0
        
        with col1:
            st.markdown(f"""
            <div class="main-metric">
                <div class="metric-label">🎯 OBJECTIFS</div>
                <div class="metric-value">{total_objectifs}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="main-metric" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <div class="metric-label">✅ RÉALISÉS</div>
                <div class="metric-value">{total_livres}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="main-metric" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <div class="metric-label">📊 TAUX GLOBAL</div>
                <div class="metric-value">{taux_global:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="main-metric" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                <div class="metric-label">📈 RÉALISATIONS</div>
                <div class="metric-value">{int(total_realisations)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # SECTION 2 : GRAPHIQUES
        st.markdown("## 📊 ANALYSES DÉTAILLÉES")
        
        col1, col2 = st.columns(2)
        
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
                marker=dict(color=mois_values, colorscale='Viridis', line=dict(color='darkblue', width=2)),
                text=mois_values,
                textposition='auto',
                hovertemplate='<b>%{x}</b><br>Réalisations: %{y}<extra></extra>'
            ))
            fig1.update_layout(
                title="📈 Progression Mensuelle",
                xaxis_title="Mois",
                yaxis_title="Réalisations",
                height=400,
                template='plotly_white'
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
                marker=dict(color=top_livs['Total'], colorscale='Reds', line=dict(color='darkred', width=2)),
                text=top_livs['Total'],
                textposition='auto'
            ))
            fig2.update_layout(
                title="🏆 Top 10 Livrables",
                xaxis_title="Réalisations",
                height=400,
                template='plotly_white'
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Graphique 3 : Jauge
        col1, col2 = st.columns(2)
        
        with col1:
            fig3 = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=taux_global,
                title={'text': "Taux Réalisation Global"},
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
        
        # Graphique 4 : Radar
        with col2:
            # Calculer le taux par section (A, B, C)
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
                    name='Réalisation',
                    line=dict(color='#667eea'),
                    fillcolor='rgba(102, 126, 234, 0.3)'
                ))
                fig4.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                    height=400,
                    template='plotly_white'
                )
                st.plotly_chart(fig4, use_container_width=True)
        
        # SECTION 3 : TABLEAU DÉTAILLÉ
        st.divider()
        st.markdown("## 📋 TABLEAU DÉTAILLÉ")
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # AUTO-REFRESH
        if auto_refresh:
            st.info("🔄 Auto-refresh activé - Mise à jour toutes les 30 secondes")
            time.sleep(30)
            st.rerun()
        
    except Exception as e:
        st.error(f"❌ Erreur : {str(e)}")

else:
    st.info("👈 Entrez le lien de votre Google Sheet")

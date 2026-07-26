import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ============================================================================
# CONFIG STREAMLIT
# ============================================================================

st.set_page_config(
    page_title="DSVCo — Tableau de Bord S1 2026",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# COULEURS INSTITUTIONNELLES
# ============================================================================

COLORS = {
    "primary": "#0B3A5B",
    "secondary": "#1976D2",
    "success": "#2E7D32",
    "warning": "#F57C00",
    "danger": "#D32F2F",
    "info": "#0288D1",
    "light": "#F5F7FA",
    "border": "#E0E7FF",
    "text": "#1F2937",
    "text_light": "#6B7280",
    "gouvernance": "#1565C0",
    "supervision": "#EF6C00",
    "prioritaires": "#2E7D32"
}

# ============================================================================
# CSS PERSONNALISÉ — DESIGN PREMIUM
# ============================================================================

st.markdown(f"""
<style>
    * {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', sans-serif; }}
    
    .stApp {{ background-color: {COLORS['light']}; }}
    
    /* HEADER */
    .header-container {{
        background: {COLORS['primary']};
        color: white;
        padding: 40px 30px;
        border-radius: 0;
        margin: -70px -30px 30px -30px;
        padding-top: 50px;
    }}
    
    .header-title {{
        font-size: 32px;
        font-weight: 800;
        margin: 0;
        padding: 0;
        letter-spacing: -0.5px;
    }}
    
    .header-subtitle {{
        font-size: 14px;
        opacity: 0.95;
        margin-top: 8px;
        font-weight: 400;
    }}
    
    .header-meta {{
        font-size: 12px;
        opacity: 0.8;
        margin-top: 12px;
    }}
    
    /* KPI CARDS */
    .kpi-card {{
        background: white;
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        padding: 24px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        text-align: center;
        transition: all 0.3s ease;
    }}
    
    .kpi-card:hover {{
        border-color: {COLORS['secondary']};
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }}
    
    .kpi-value {{
        font-size: 42px;
        font-weight: 800;
        color: {COLORS['primary']};
        margin: 12px 0;
        line-height: 1;
    }}
    
    .kpi-label {{
        font-size: 12px;
        color: {COLORS['text_light']};
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }}
    
    .kpi-info {{
        font-size: 11px;
        color: {COLORS['text_light']};
        margin-top: 8px;
    }}
    
    /* PERFORMANCE CARDS */
    .perf-card {{
        background: white;
        border-left: 4px solid {COLORS['secondary']};
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin-bottom: 16px;
    }}
    
    .perf-card.success {{ border-left-color: {COLORS['success']}; }}
    .perf-card.warning {{ border-left-color: {COLORS['warning']}; }}
    .perf-card.danger {{ border-left-color: {COLORS['danger']}; }}
    
    /* SECTION CARDS */
    .section-card {{
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }}
    
    .section-header {{
        padding: 20px;
        color: white;
        font-weight: 700;
        font-size: 16px;
    }}
    
    .section-header.gouvernance {{ background: {COLORS['gouvernance']}; }}
    .section-header.supervision {{ background: {COLORS['supervision']}; }}
    .section-header.prioritaires {{ background: {COLORS['prioritaires']}; }}
    
    .section-content {{
        padding: 20px;
    }}
    
    .metric-small {{
        display: flex;
        justify-content: space-around;
        gap: 12px;
        margin-bottom: 16px;
    }}
    
    .metric-small-item {{
        flex: 1;
        text-align: center;
    }}
    
    .metric-small-value {{
        font-size: 28px;
        font-weight: 700;
        color: {COLORS['primary']};
    }}
    
    .metric-small-label {{
        font-size: 11px;
        color: {COLORS['text_light']};
        text-transform: uppercase;
        margin-top: 6px;
        font-weight: 600;
    }}
    
    .progress-container {{
        margin: 12px 0;
    }}
    
    .progress-bar {{
        width: 100%;
        height: 8px;
        background: {COLORS['border']};
        border-radius: 4px;
        overflow: hidden;
        margin: 8px 0;
    }}
    
    .progress-fill {{
        height: 100%;
        border-radius: 4px;
        transition: width 0.5s ease;
    }}
    
    .status-badge {{
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        margin-top: 8px;
    }}
    
    .status-good {{
        background: #ECFDF5;
        color: #065F46;
    }}
    
    .status-warning {{
        background: #FFFBEB;
        color: #92400E;
    }}
    
    .status-danger {{
        background: #FEF2F2;
        color: #991B1B;
    }}
    
    /* TABS */
    .stTabs [data-baseweb="tab-list"] {{
        border-bottom: 1px solid {COLORS['border']};
    }}
    
    /* ATTENTION SECTION */
    .attention-item {{
        background: #FFFBEB;
        border-left: 3px solid {COLORS['warning']};
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 8px;
        font-size: 13px;
    }}
    
    .attention-item.danger {{
        background: #FEF2F2;
        border-left-color: {COLORS['danger']};
    }}
    
    /* SECTION TITLE */
    .section-title {{
        font-size: 20px;
        font-weight: 700;
        color: {COLORS['primary']};
        margin-top: 40px;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 2px solid {COLORS['secondary']};
    }}
    
    /* FOOTER */
    .footer {{
        text-align: center;
        font-size: 11px;
        color: {COLORS['text_light']};
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid {COLORS['border']};
    }}
    
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FONCTIONS DE CHARGEMENT ET TRAITEMENT
# ============================================================================

@st.cache_data(ttl=300)
def load_data():
    """Charger les données du Google Sheet"""
    sheet_url = "https://docs.google.com/spreadsheets/d/1BVEEDaDQZ9cauGKau03BFc7rvmUoOX8aiUDOHQTqyV0/edit?usp=sharing"
    sheet_id = sheet_url.split('/d/')[1].split('/')[0]
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
    
    df = pd.read_csv(csv_url)
    return df

def prepare_data(df):
    """Préparer les données"""
    mois = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin']
    
    # Convertir les colonnes mois en numérique
    for col in mois:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    
    df['Total'] = df[mois].sum(axis=1)
    
    return df, mois

def separate_by_section(df):
    """Séparer les données par section"""
    col_n = 'N°' if 'N°' in df.columns else df.columns[0]
    
    # Section A (1-10)
    df_a = df[df[col_n].astype(str).str.strip().apply(lambda x: str(x).isdigit() and 1 <= int(x) <= 10)]
    
    # Section B (B1-B5)
    df_b = df[df[col_n].astype(str).str.contains('B', na=False, regex=False)]
    
    # Section C (C1-C5)
    df_c = df[df[col_n].astype(str).str.contains('C', na=False, regex=False)]
    
    return df_a, df_b, df_c

def calculate_section_metrics(df_section, mois):
    """Calculer les métriques d'une section"""
    if len(df_section) == 0:
        return {
            'objectifs': 0,
            'realises': 0,
            'non_realises': 0,
            'taux': 0,
            'actions': 0,
            'statut': 'N/A'
        }
    
    total_obj = len(df_section)
    total_realises = len(df_section[df_section['Total'] > 0])
    total_non_realises = total_obj - total_realises
    taux = (total_realises / total_obj * 100) if total_obj > 0 else 0
    total_actions = int(df_section[mois].sum().sum())
    
    # Déterminer le statut
    if taux >= 80:
        statut = "Bonne performance"
    elif taux >= 50:
        statut = "À surveiller"
    else:
        statut = "Retard"
    
    return {
        'objectifs': total_obj,
        'realises': total_realises,
        'non_realises': total_non_realises,
        'taux': taux,
        'actions': total_actions,
        'statut': statut
    }

def get_status_class(taux):
    """Déterminer la classe CSS pour le statut"""
    if taux >= 80:
        return "success"
    elif taux >= 50:
        return "warning"
    else:
        return "danger"

# ============================================================================
# COMPOSANTS VISUELS
# ============================================================================

def render_header():
    """Rendu du header institutionnel"""
    st.markdown(f"""
    <div class="header-container">
        <div class="header-title">TABLEAU DE BORD DE SUIVI</div>
        <div class="header-subtitle">Lettre de mission 2026</div>
        <div class="header-subtitle">Direction de la Santé de la Ville de Conakry — DSVCo</div>
        <div class="header-meta">
            🔄 Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y à %H:%M')} 
            | Période : Janvier → Juin 2026
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_global_kpis(df, mois):
    """Rendu des KPI globaux"""
    total_obj = len(df)
    total_realises = len(df[df['Total'] > 0])
    taux_global = (total_realises / total_obj * 100) if total_obj > 0 else 0
    total_actions = int(df[mois].sum().sum())
    
    status_text = "Bonne" if taux_global >= 80 else "À surveiller" if taux_global >= 50 else "Faible"
    
    col1, col2, col3, col4, col5 = st.columns(5, gap="small")
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">📋 Objectifs</div>
            <div class="kpi-value">{total_obj}</div>
            <div class="kpi-info">Total cible</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">✅ Réalisés</div>
            <div class="kpi-value">{total_realises}</div>
            <div class="kpi-info">{total_obj - total_realises} en attente</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">📈 Taux</div>
            <div class="kpi-value">{taux_global:.0f}%</div>
            <div class="kpi-info">Réalisation globale</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">🔄 Actions</div>
            <div class="kpi-value">{total_actions}</div>
            <div class="kpi-info">Réalisées S1</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        color = COLORS['success'] if taux_global >= 80 else COLORS['warning'] if taux_global >= 50 else COLORS['danger']
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">⚡ Performance</div>
            <div class="kpi-value" style="color: {color}; font-size: 28px;">●</div>
            <div class="kpi-info">{status_text}</div>
        </div>
        """, unsafe_allow_html=True)

def render_section_card(df_section, section_name, section_class, color_hex):
    """Rendu d'une carte de section"""
    metrics = calculate_section_metrics(df_section, ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin'])
    status_class = get_status_class(metrics['taux'])
    
    status_badge_class = f"status-{status_class}"
    status_text = metrics['statut']
    
    st.markdown(f"""
    <div class="section-card">
        <div class="section-header {section_class}">{section_name}</div>
        <div class="section-content">
            <div class="metric-small">
                <div class="metric-small-item">
                    <div class="metric-small-value">{metrics['objectifs']}</div>
                    <div class="metric-small-label">Objectifs</div>
                </div>
                <div class="metric-small-item">
                    <div class="metric-small-value">{metrics['realises']}</div>
                    <div class="metric-small-label">Réalisés</div>
                </div>
                <div class="metric-small-item">
                    <div class="metric-small-value">{metrics['non_realises']}</div>
                    <div class="metric-small-label">En attente</div>
                </div>
                <div class="metric-small-item">
                    <div class="metric-small-value">{metrics['actions']}</div>
                    <div class="metric-small-label">Actions</div>
                </div>
            </div>
            
            <div class="progress-container">
                <strong style="font-size: 13px; color: {COLORS['text']};">{metrics['taux']:.0f}% Réalisé</strong>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {metrics['taux']}%; background: {color_hex};"></div>
                </div>
            </div>
            
            <div style="text-align: center;">
                <span class="{status_badge_class}" style="margin: 0;">● {status_text}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_attention_items(df_a, df_b, df_c):
    """Rendu des points d'attention"""
    st.markdown('<div class="section-title">⚠️ Points d\'attention</div>', unsafe_allow_html=True)
    
    attention_items = []
    
    # Ajouter toutes les activités sans réalisation
    for section_name, df_section in [("Gouvernance", df_a), ("Supervision", df_b), ("Prioritaires", df_c)]:
        for _, row in df_section.iterrows():
            if row['Total'] == 0:
                attention_items.append({
                    'livrable': row.get('Livrable', 'N/A'),
                    'section': section_name,
                    'status': 'Non démarré',
                    'severity': 'danger'
                })
    
    if attention_items:
        for item in attention_items[:10]:
            st.markdown(f"""
            <div class="attention-item {item['severity']}">
                <strong>{item['livrable'][:60]}</strong><br>
                <small>{item['section']} • {item['status']}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("✅ Aucune activité en retard. Tous les livrables sont en cours ou réalisés.")

def apply_plotly_theme(fig):
    """Appliquer le thème aux graphiques Plotly"""
    fig.update_layout(
        font=dict(family="system-ui, -apple-system, sans-serif", size=12, color=COLORS['text']),
        plot_bgcolor="rgba(245, 247, 250, 0.5)",
        paper_bgcolor="white",
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode='x unified',
        showlegend=True,
        legend=dict(orientation="h", x=0, y=1.1, bgcolor="rgba(0,0,0,0)")
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(224, 231, 255, 0.5)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(224, 231, 255, 0.5)")
    
    return fig

# ============================================================================
# APPLICATION PRINCIPALE
# ============================================================================

def main():
    # Header
    render_header()
    
    try:
        # Charger et préparer les données
        df = load_data()
        df, mois = prepare_data(df)
        df_a, df_b, df_c = separate_by_section(df)
        
        # Synthèse globale
        render_global_kpis(df, mois)
        
        # Trois sections de performance
        st.markdown('<div class="section-title">📊 Performance par axe</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3, gap="medium")
        
        with col1:
            render_section_card(df_a, "A. GOUVERNANCE", "gouvernance", COLORS['gouvernance'])
        
        with col2:
            render_section_card(df_b, "B. AXE DE SUPERVISION", "supervision", COLORS['supervision'])
        
        with col3:
            render_section_card(df_c, "C. ACTIVITÉS PRIORITAIRES", "prioritaires", COLORS['prioritaires'])
        
        # Analyse visuelle
        st.markdown('<div class="section-title">📈 Analyse de la performance</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1.5, 1], gap="medium")
        
        # Graphique comparatif
        with col1:
            metrics_a = calculate_section_metrics(df_a, mois)
            metrics_b = calculate_section_metrics(df_b, mois)
            metrics_c = calculate_section_metrics(df_c, mois)
            
            fig_compare = go.Figure()
            
            fig_compare.add_trace(go.Bar(
                y=['Gouvernance', 'Supervision', 'Prioritaires'],
                x=[metrics_a['taux'], metrics_b['taux'], metrics_c['taux']],
                orientation='h',
                marker=dict(color=[COLORS['gouvernance'], COLORS['supervision'], COLORS['prioritaires']]),
                text=[f"{metrics_a['taux']:.0f}%", f"{metrics_b['taux']:.0f}%", f"{metrics_c['taux']:.0f}%"],
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Taux : %{x:.1f}%<extra></extra>',
                showlegend=False
            ))
            
            fig_compare.update_layout(
                title="<b>Comparaison des taux de réalisation</b>",
                xaxis_title="Taux (%)",
                xaxis=dict(range=[0, 110]),
                height=350
            )
            
            st.plotly_chart(apply_plotly_theme(fig_compare), use_container_width=True)
        
        # Répartition
        with col2:
            total_realises_all = len(df[df['Total'] > 0])
            total_non_realises_all = len(df[df['Total'] == 0])
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=['Réalisés', 'En attente'],
                values=[total_realises_all, total_non_realises_all],
                marker=dict(colors=[COLORS['success'], COLORS['warning']]),
                hovertemplate='<b>%{label}</b><br>%{value} activités<extra></extra>'
            )])
            
            fig_pie.update_layout(
                title="<b>Répartition des livrables</b>",
                height=350
            )
            
            st.plotly_chart(apply_plotly_theme(fig_pie), use_container_width=True)
        
        # Points d'attention
        render_attention_items(df_a, df_b, df_c)
        
        # Détail des activités
        st.markdown('<div class="section-title">📋 Détail des activités</div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Gouvernance", "Supervision", "Prioritaires"])
        
        with tab1:
            if len(df_a) > 0:
                col_liv = 'Livrable' if 'Livrable' in df_a.columns else df_a.columns[1]
                st.dataframe(
                    df_a[[col_liv] + mois + ['Total']].assign(**{
                        'Statut': df_a['Total'].apply(lambda x: '✅ Réalisé' if x > 0 else '⏳ En attente')
                    }),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("Aucune donnée pour Gouvernance")
        
        with tab2:
            if len(df_b) > 0:
                col_liv = 'Livrable' if 'Livrable' in df_b.columns else df_b.columns[1]
                st.dataframe(
                    df_b[[col_liv] + mois + ['Total']].assign(**{
                        'Statut': df_b['Total'].apply(lambda x: '✅ Réalisé' if x > 0 else '⏳ En attente')
                    }),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("Aucune donnée pour Supervision")
        
        with tab3:
            if len(df_c) > 0:
                col_liv = 'Livrable' if 'Livrable' in df_c.columns else df_c.columns[1]
                st.dataframe(
                    df_c[[col_liv] + mois + ['Total']].assign(**{
                        'Statut': df_c['Total'].apply(lambda x: '✅ Réalisé' if x > 0 else '⏳ En attente')
                    }),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("Aucune donnée pour Prioritaires")
        
        # Footer
        st.markdown(f"""
        <div class="footer">
            Dashboard DSVCo • Lettre de mission S1 2026<br>
            Données synchronisées en temps réel depuis Google Sheets
        </div>
        """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"❌ Erreur de chargement : {str(e)}")
        st.info("Vérifiez que le Google Sheet est accessible et contient les bonnes données.")

if __name__ == "__main__":
    main()

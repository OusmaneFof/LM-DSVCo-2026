import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
import time

# ============================================================================
# CONFIGURATION STREAMLIT
# ============================================================================

st.set_page_config(
    page_title="DSVCo — Tableau de Bord de Suivi S1 2026",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# THÈME ET COULEURS INSTITUTIONNELLES
# ============================================================================

COLORS = {
    "primary_dark": "#0B3A5B",
    "primary": "#1976D2",
    "gouvernance": "#1565C0",
    "prioritaires": "#2E7D32",
    "supervision": "#EF6C00",
    "success": "#4CAF50",
    "warning": "#FFA726",
    "danger": "#D32F2F",
    "text_primary": "#1F2937",
    "text_secondary": "#64748B",
    "border": "#E2E8F0",
    "background": "#F6F8FB",
    "white": "#FFFFFF"
}

THRESHOLDS = {
    "good": 80,
    "warning": 50
}

# ============================================================================
# CSS PERSONNALISÉ — DESIGN PREMIUM
# ============================================================================

st.markdown(f"""
<style>
    * {{
        font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}
    
    .stApp {{
        background-color: {COLORS['background']};
    }}
    
    /* HEADER PREMIUM */
    .header-container {{
        background: {COLORS['white']};
        padding: 20px 30px;
        border-bottom: 1px solid {COLORS['border']};
        border-radius: 8px;
        margin-bottom: 30px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }}
    
    .header-title {{
        font-size: 24px;
        font-weight: 700;
        color: {COLORS['primary_dark']};
        margin: 0;
        padding: 0;
    }}
    
    .header-subtitle {{
        font-size: 13px;
        color: {COLORS['text_secondary']};
        margin: 4px 0 0 0;
        font-weight: 400;
    }}
    
    .header-status {{
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 12px;
        color: {COLORS['text_secondary']};
    }}
    
    .status-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        background: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 20px;
        font-size: 12px;
        color: #166534;
        font-weight: 500;
    }}
    
    /* CARTES KPI GLOBALES */
    .kpi-card {{
        background: {COLORS['white']};
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}
    
    .kpi-card:hover {{
        border-color: {COLORS['primary']};
        box-shadow: 0 4px 12px rgba(25,118,210,0.1);
    }}
    
    .kpi-value {{
        font-size: 36px;
        font-weight: 700;
        color: {COLORS['primary_dark']};
        margin: 8px 0;
    }}
    
    .kpi-label {{
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: {COLORS['text_secondary']};
        font-weight: 500;
    }}
    
    .kpi-icon {{
        font-size: 24px;
        margin-bottom: 8px;
    }}
    
    .kpi-status {{
        font-size: 11px;
        font-weight: 600;
        margin-top: 8px;
        padding: 6px 12px;
        border-radius: 12px;
        display: inline-block;
    }}
    
    .status-good {{
        background: #F0FDF4;
        color: #166534;
    }}
    
    .status-warning {{
        background: #FEF3C7;
        color: #92400E;
    }}
    
    .status-danger {{
        background: #FEE2E2;
        color: #991B1B;
    }}
    
    /* SECTION CARDS */
    .section-card {{
        background: {COLORS['white']};
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        height: 100%;
    }}
    
    .section-header {{
        font-size: 16px;
        font-weight: 700;
        color: {COLORS['white']};
        padding: 12px 16px;
        border-radius: 8px;
        margin: -24px -24px 20px -24px;
    }}
    
    .section-header-a {{
        background: linear-gradient(135deg, #1565C0 0%, #1976D2 100%);
    }}
    
    .section-header-b {{
        background: linear-gradient(135deg, #2E7D32 0%, #43A047 100%);
    }}
    
    .section-header-c {{
        background: linear-gradient(135deg, #EF6C00 0%, #F57C00 100%);
    }}
    
    .metric-row {{
        display: flex;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 16px;
        flex-wrap: wrap;
    }}
    
    .metric-item {{
        flex: 1;
        min-width: 120px;
    }}
    
    .metric-small-value {{
        font-size: 24px;
        font-weight: 700;
        color: {COLORS['primary_dark']};
    }}
    
    .metric-small-label {{
        font-size: 11px;
        color: {COLORS['text_secondary']};
        margin-top: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    .progress-bar {{
        width: 100%;
        height: 6px;
        background: {COLORS['border']};
        border-radius: 3px;
        overflow: hidden;
        margin: 12px 0;
    }}
    
    .progress-fill {{
        height: 100%;
        border-radius: 3px;
        transition: width 0.5s ease;
    }}
    
    .performance-badge {{
        display: inline-block;
        font-size: 11px;
        font-weight: 600;
        padding: 6px 12px;
        border-radius: 12px;
        margin-top: 12px;
    }}
    
    /* TABLEAU DÉTAIL */
    .tab-section {{
        margin-top: 40px;
    }}
    
    /* RESPONSIVE */
    @media (max-width: 1366px) {{
        .kpi-value {{
            font-size: 28px;
        }}
    }}
    
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

@st.cache_data(ttl=600)
def load_data():
    """Charger les données depuis Google Sheets"""
    sheet_url = "https://docs.google.com/spreadsheets/d/1BVEEDaDQZ9cauGKau03BFc7rvmUoOX8aiUDOHQTqyV0/edit?usp=sharing"
    sheet_id = sheet_url.split('/d/')[1].split('/')[0]
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
    
    df = pd.read_csv(csv_url)
    return df

def prepare_data(df):
    """Préparer et nettoyer les données"""
    mois = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin']
    
    for col in mois:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    df['Total'] = df[mois].sum(axis=1)
    return df, mois

def get_performance_status(taux):
    """Déterminer le statut de performance"""
    if taux >= THRESHOLDS['good']:
        return "Bonne performance", "status-good", "✓"
    elif taux >= THRESHOLDS['warning']:
        return "À surveiller", "status-warning", "!"
    else:
        return "Retard", "status-danger", "✕"

def separate_sections(df):
    """Séparer les données par rubrique"""
    col_n = 'N°' if 'N°' in df.columns else df.columns[0]
    
    df_a = df[df[col_n].astype(str).str.strip().apply(lambda x: x.isdigit() and 1 <= int(x) <= 10)]
    df_b = df[df[col_n].astype(str).str.contains('B', na=False)]
    df_c = df[df[col_n].astype(str).str.contains('C', na=False)]
    
    return df_a, df_b, df_c

def calculate_metrics(df_section, mois):
    """Calculer les métriques d'une section"""
    total_objectifs = len(df_section)
    total_realises = len(df_section[df_section['Total'] > 0])
    taux = (total_realises / total_objectifs * 100) if total_objectifs > 0 else 0
    total_actions = int(df_section[mois].sum().sum())
    
    return {
        'objectifs': total_objectifs,
        'realises': total_realises,
        'taux': taux,
        'actions': total_actions
    }

def apply_plotly_theme(fig):
    """Appliquer le thème personnalisé aux graphiques Plotly"""
    fig.update_layout(
        font=dict(family="Inter, Roboto, sans-serif", size=12, color=COLORS['text_primary']),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode='x unified',
        showlegend=True,
        legend=dict(orientation="h", x=0, y=1.15, bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)")
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(226, 232, 240, 0.5)", showline=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(226, 232, 240, 0.5)", showline=False)
    
    return fig

# ============================================================================
# COMPOSANTS VISUELS
# ============================================================================

def render_header():
    """Rendu du header professionnel"""
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"""
        <div class="header-container">
            <p class="header-title">TABLEAU DE BORD DE SUIVI</p>
            <p class="header-subtitle">Direction de la Santé de la Ville de Conakry • Lettre de mission — S1 2026</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        col_a, col_b = st.columns([1, 1])
        with col_a:
            st.markdown(f"""
            <div style="text-align: right; padding-top: 20px;">
                <p style="font-size: 13px; color: {COLORS['text_secondary']}; margin: 0;">Janvier → Juin 2026</p>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown(f"""
            <div style="text-align: right; padding-top: 15px;">
                <div class="status-badge">
                    <span style="width: 8px; height: 8px; background: #22C55E; border-radius: 50%; display: inline-block;"></span>
                    Données à jour
                </div>
                <p style="font-size: 11px; color: {COLORS['text_secondary']}; margin-top: 6px; margin-bottom: 0;">
                    Sync : {datetime.now().strftime('%H:%M')}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("↻ Actualiser", key="refresh_btn"):
                st.cache_data.clear()
                st.rerun()

def render_global_kpis(df, mois):
    """Rendu des KPI globaux"""
    total_objectifs = len(df)
    total_realises = len(df[df['Total'] > 0])
    taux_global = (total_realises / total_objectifs * 100) if total_objectifs > 0 else 0
    total_actions = int(df[mois].sum().sum())
    
    status_text, status_class, status_icon = get_performance_status(taux_global)
    
    col1, col2, col3, col4, col5 = st.columns(5, gap="small")
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Objectifs</div>
            <div class="kpi-value">{total_objectifs}</div>
            <div style="font-size: 11px; color: {COLORS['text_secondary']};">Total cible</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Réalisés</div>
            <div class="kpi-value">{total_realises}</div>
            <div style="font-size: 11px; color: {COLORS['text_secondary']};">En cours</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Taux d'exécution</div>
            <div class="kpi-value">{taux_global:.0f}%</div>
            <div style="font-size: 11px; color: {COLORS['text_secondary']};">Globalement</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Actions</div>
            <div class="kpi-value">{total_actions}</div>
            <div style="font-size: 11px; color: {COLORS['text_secondary']};">Réalisées</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Performance</div>
            <div class="kpi-value" style="font-size: 20px;">{status_icon}</div>
            <div class="kpi-status {status_class}">{status_text}</div>
        </div>
        """, unsafe_allow_html=True)

def render_section_card(df_section, mois, title, color_header, color_primary, color_rgba):
    """Rendu d'une carte de section"""
    metrics = calculate_metrics(df_section, mois)
    status_text, status_class, _ = get_performance_status(metrics['taux'])
    
    mois_values = [df_section[m].sum() for m in mois]
    
    st.markdown(f"""
    <div class="section-card">
        <div class="section-header {color_header}">{title}</div>
        
        <div class="metric-row">
            <div class="metric-item">
                <div class="metric-small-value">{metrics['objectifs']}</div>
                <div class="metric-small-label">Objectifs</div>
            </div>
            <div class="metric-item">
                <div class="metric-small-value">{metrics['realises']}</div>
                <div class="metric-small-label">Réalisés</div>
            </div>
            <div class="metric-item">
                <div class="metric-small-value">{metrics['taux']:.0f}%</div>
                <div class="metric-small-label">Taux</div>
            </div>
            <div class="metric-item">
                <div class="metric-small-value">{metrics['actions']}</div>
                <div class="metric-small-label">Actions</div>
            </div>
        </div>
        
        <div class="progress-bar">
            <div class="progress-fill" style="width: {metrics['taux']}%; background: {color_primary};"></div>
        </div>
        
        <div class="performance-badge" style="background: #F0F9FF; color: {color_primary}; border: 1px solid {color_rgba.replace('0.2', '0.5')};">
            ● {status_text}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Mini sparkline
    fig_spark = go.Figure()
    fig_spark.add_trace(go.Scatter(
        x=mois,
        y=mois_values,
        mode='lines',
        line=dict(color=color_primary, width=2),
        fill='tozeroy',
        fillcolor=color_rgba,
        hovertemplate='<b>%{x}</b><br>Réalisations: %{y}<extra></extra>',
        showlegend=False,
        name=''
    ))
    
    fig_spark.update_layout(
        height=60,
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, showline=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, showline=False, zeroline=False, showticklabels=False),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_spark, use_container_width=True, config={'displayModeBar': False})

# ============================================================================
# GRAPHIQUES STRATÉGIQUES
# ============================================================================

def create_monthly_comparison_chart(df_a, df_b, df_c, mois):
    """Graphique : Évolution mensuelle comparée"""
    values_a = [df_a[m].sum() for m in mois]
    values_b = [df_b[m].sum() for m in mois]
    values_c = [df_c[m].sum() for m in mois]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=mois,
        y=values_a,
        mode='lines+markers',
        name='Gouvernance',
        line=dict(color=COLORS['gouvernance'], width=3),
        marker=dict(size=8),
        hovertemplate='<b>Gouvernance — %{x}</b><br>Actions: %{y}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=mois,
        y=values_b,
        mode='lines+markers',
        name='Activités prioritaires',
        line=dict(color=COLORS['prioritaires'], width=3),
        marker=dict(size=8),
        hovertemplate='<b>Prioritaires — %{x}</b><br>Actions: %{y}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=mois,
        y=values_c,
        mode='lines+markers',
        name='Axe de supervision',
        line=dict(color=COLORS['supervision'], width=3),
        marker=dict(size=8),
        hovertemplate='<b>Supervision — %{x}</b><br>Actions: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title="<b>Évolution mensuelle des réalisations par rubrique</b>",
        xaxis_title="Mois",
        yaxis_title="Nombre d'actions réalisées",
        height=400
    )
    
    return apply_plotly_theme(fig)

def create_performance_comparison_chart(df_a, df_b, df_c):
    """Graphique : Performance comparée (barres horizontales)"""
    metrics_a = calculate_metrics(df_a, ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin'])
    metrics_b = calculate_metrics(df_b, ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin'])
    metrics_c = calculate_metrics(df_c, ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin'])
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=['Gouvernance', 'Prioritaires', 'Supervision'],
        x=[metrics_a['taux'], metrics_b['taux'], metrics_c['taux']],
        orientation='h',
        marker=dict(color=[COLORS['gouvernance'], COLORS['prioritaires'], COLORS['supervision']]),
        text=[f"{metrics_a['taux']:.0f}%", f"{metrics_b['taux']:.0f}%", f"{metrics_c['taux']:.0f}%"],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Taux: %{x:.1f}%<extra></extra>',
        showlegend=False
    ))
    
    fig.update_layout(
        title="<b>Performance par rubrique</b>",
        xaxis_title="Taux de réalisation (%)",
        xaxis=dict(range=[0, 110]),
        height=350
    )
    
    return apply_plotly_theme(fig)

def create_monthly_volume_chart(df, mois):
    """Graphique : Volume mensuel total"""
    monthly_values = [df[m].sum() for m in mois]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=mois,
        y=monthly_values,
        marker=dict(color=COLORS['primary'], line=dict(color=COLORS['primary_dark'], width=1)),
        text=monthly_values,
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Actions réalisées: %{y}<extra></extra>',
        showlegend=False
    ))
    
    fig.update_layout(
        title="<b>Réalisations mensuelles</b>",
        xaxis_title="Mois",
        yaxis_title="Nombre d'actions",
        height=350
    )
    
    return apply_plotly_theme(fig)

# ============================================================================
# APPLICATION PRINCIPALE
# ============================================================================

def main():
    render_header()
    
    try:
        # Charger et préparer les données
        df = load_data()
        df, mois = prepare_data(df)
        df_a, df_b, df_c = separate_sections(df)
        
        # KPI GLOBAUX
        st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)
        render_global_kpis(df, mois)
        
        # TROIS CARTES DE SECTION
        st.markdown("<div style='margin-top: 40px; margin-bottom: 20px;'></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3, gap="medium")
        
        with col1:
            if len(df_a) > 0:
                render_section_card(df_a, mois, "A. GOUVERNANCE", "section-header-a", COLORS['gouvernance'], "rgba(21, 101, 192, 0.2)")
        
        with col2:
            if len(df_b) > 0:
                render_section_card(df_b, mois, "B. ACTIVITÉS PRIORITAIRES", "section-header-b", COLORS['prioritaires'], "rgba(46, 125, 50, 0.2)")
        
        with col3:
            if len(df_c) > 0:
                render_section_card(df_c, mois, "C. AXE DE SUPERVISION", "section-header-c", COLORS['supervision'], "rgba(239, 108, 0, 0.2)")
        
        # GRAPHIQUES STRATÉGIQUES
        st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color: {COLORS['primary_dark']}; font-size: 18px; font-weight: 700;'>Analyses Stratégiques</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1.5, 1], gap="medium")
        
        with col1:
            fig_evolution = create_monthly_comparison_chart(df_a, df_b, df_c, mois)
            st.plotly_chart(fig_evolution, use_container_width=True)
        
        with col2:
            fig_performance = create_performance_comparison_chart(df_a, df_b, df_c)
            st.plotly_chart(fig_performance, use_container_width=True)
        
        # VOLUME MENSUEL
        col1, col2 = st.columns([1, 1], gap="medium")
        
        with col1:
            fig_monthly = create_monthly_volume_chart(df, mois)
            st.plotly_chart(fig_monthly, use_container_width=True)
        
        with col2:
            # Activités à surveiller
            st.markdown(f"""
            <div style='background: {COLORS['white']}; border: 1px solid {COLORS['border']}; border-radius: 12px; padding: 24px;'>
                <h3 style='margin-top: 0; color: {COLORS['primary_dark']}; font-size: 15px; font-weight: 700;'>Activités à surveiller</h3>
            </div>
            """, unsafe_allow_html=True)
            
            attention_items = []
            
            for _, row in df.iterrows():
                if row['Total'] == 0:
                    attention_items.append({
                        'livrable': row.get('Livrable', 'N/A'),
                        'statut': 'Retard',
                        'color': COLORS['danger']
                    })
            
            if attention_items:
                for item in attention_items[:5]:
                    st.markdown(f"""
                    <div style='padding: 12px; border-left: 3px solid {item['color']}; background: {COLORS['background']}; border-radius: 4px; margin-bottom: 8px; font-size: 12px;'>
                        <strong>{item['livrable'][:50]}</strong><br>
                        <span style='color: {COLORS['text_secondary']}; font-size: 11px;'>{item['statut']}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("✓ Aucune activité en retard")
        
        # DÉTAIL TABULAIRE
        st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color: {COLORS['primary_dark']}; font-size: 18px; font-weight: 700;'>Détail des activités</h3>", unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Gouvernance", "Prioritaires", "Supervision"])
        
        with tab1:
            if len(df_a) > 0:
                col_liv = 'Livrable' if 'Livrable' in df_a.columns else df_a.columns[1]
                df_display = df_a[[col_liv] + mois + ['Total']].copy()
                st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        with tab2:
            if len(df_b) > 0:
                col_liv = 'Livrable' if 'Livrable' in df_b.columns else df_b.columns[1]
                df_display = df_b[[col_liv] + mois + ['Total']].copy()
                st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        with tab3:
            if len(df_c) > 0:
                col_liv = 'Livrable' if 'Livrable' in df_c.columns else df_c.columns[1]
                df_display = df_c[[col_liv] + mois + ['Total']].copy()
                st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # FOOTER
        st.markdown("<div style='margin-top: 50px; padding-top: 20px; border-top: 1px solid #E2E8F0;'></div>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-size: 11px; color: {COLORS['text_secondary']}; margin: 0;'>Dashboard DSVCo — Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y à %H:%M')}</p>", unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"❌ Erreur de chargement : {str(e)}")
        st.info("Vérifiez que le Google Sheet est accessible et partagé publiquement.")

if __name__ == "__main__":
    main()

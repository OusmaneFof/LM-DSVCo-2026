import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="DSVCo — Tableau de Bord de Suivi S1 2026", layout="wide", initial_sidebar_state="collapsed")

COLORS = {
    "primary_dark": "#0B3A5B",
    "primary": "#1976D2",
    "gouvernance": "#1565C0",
    "prioritaires": "#2E7D32",
    "supervision": "#EF6C00",
    "text_primary": "#1F2937",
    "text_secondary": "#64748B",
    "border": "#E2E8F0",
    "background": "#F6F8FB",
    "white": "#FFFFFF"
}

st.markdown(f"""
<style>
    * {{ font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }}
    .stApp {{ background-color: {COLORS['background']}; }}
    .kpi-card {{ background: {COLORS['white']}; border: 1px solid {COLORS['border']}; border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
    .kpi-value {{ font-size: 36px; font-weight: 700; color: {COLORS['primary_dark']}; margin: 8px 0; }}
    .kpi-label {{ font-size: 12px; text-transform: uppercase; color: {COLORS['text_secondary']}; font-weight: 500; }}
    .section-card {{ background: {COLORS['white']}; border: 1px solid {COLORS['border']}; border-radius: 12px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
    .metric-row {{ display: flex; justify-content: space-between; gap: 12px; margin-bottom: 16px; flex-wrap: wrap; }}
    .metric-item {{ flex: 1; min-width: 100px; }}
    .metric-value-small {{ font-size: 24px; font-weight: 700; color: {COLORS['primary_dark']}; }}
    .metric-label-small {{ font-size: 11px; color: {COLORS['text_secondary']}; margin-top: 4px; text-transform: uppercase; }}
    .progress-bar {{ width: 100%; height: 6px; background: {COLORS['border']}; border-radius: 3px; overflow: hidden; margin: 12px 0; }}
    .progress-fill {{ height: 100%; border-radius: 3px; }}
    .badge {{ display: inline-block; font-size: 11px; font-weight: 600; padding: 6px 12px; border-radius: 12px; margin-top: 12px; }}
    .badge-good {{ background: #F0FDF4; color: #166534; }}
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=600)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/1BVEEDaDQZ9cauGKau03BFc7rvmUoOX8aiUDOHQTqyV0/edit?usp=sharing"
    sheet_id = sheet_url.split('/d/')[1].split('/')[0]
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
    df = pd.read_csv(csv_url)
    return df

def prepare_data(df):
    mois = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin']
    for col in mois:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    df['Total'] = df[mois].sum(axis=1)
    return df, mois

def separate_sections(df):
    col_n = 'N°' if 'N°' in df.columns else df.columns[0]
    try:
        df_a = df[df[col_n].astype(str).str.strip().apply(lambda x: str(x).isdigit() and 1 <= int(x) <= 10)]
        df_b = df[df[col_n].astype(str).str.contains('B', na=False)]
        df_c = df[df[col_n].astype(str).str.contains('C', na=False)]
    except:
        df_a = df.iloc[0:1]
        df_b = df.iloc[1:2]
        df_c = df.iloc[2:3]
    return df_a, df_b, df_c

def calculate_metrics(df_section, mois):
    total_objectifs = len(df_section)
    total_realises = len(df_section[df_section['Total'] > 0])
    taux = (total_realises / total_objectifs * 100) if total_objectifs > 0 else 0
    total_actions = int(df_section[mois].sum().sum())
    return {'objectifs': total_objectifs, 'realises': total_realises, 'taux': taux, 'actions': total_actions}

def get_performance_status(taux):
    if taux >= 80:
        return "Bonne performance", "badge-good"
    elif taux >= 50:
        return "À surveiller", "badge-warning"
    else:
        return "Retard", "badge-danger"

def apply_plotly_theme(fig):
    fig.update_layout(
        font=dict(family="Inter, Roboto, sans-serif", size=12, color=COLORS['text_primary']),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode='x unified',
        showlegend=True,
        legend=dict(orientation="h", x=0, y=1.1, bgcolor="rgba(0,0,0,0)")
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(226, 232, 240, 0.5)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(226, 232, 240, 0.5)")
    return fig

# HEADER
st.markdown(f"""
<div style="background: {COLORS['white']}; padding: 20px 30px; border-bottom: 1px solid {COLORS['border']}; border-radius: 8px; margin-bottom: 30px; box-shadow: 0 1px 3px rgba(0,0,0,0.08);">
    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
            <h1 style="font-size: 24px; font-weight: 700; color: {COLORS['primary_dark']}; margin: 0; padding: 0;">TABLEAU DE BORD DE SUIVI</h1>
            <p style="font-size: 13px; color: {COLORS['text_secondary']}; margin: 4px 0 0 0;">Direction de la Santé de la Ville de Conakry • Lettre de mission — S1 2026</p>
        </div>
        <div style="text-align: right;">
            <p style="font-size: 13px; color: {COLORS['text_secondary']}; margin: 0;">Janvier → Juin 2026</p>
            <div style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 20px; font-size: 12px; color: #166534; font-weight: 500; margin-top: 8px;">
                <span style="width: 8px; height: 8px; background: #22C55E; border-radius: 50%;"></span>
                Données à jour
            </div>
            <p style="font-size: 11px; color: {COLORS['text_secondary']}; margin-top: 6px; margin-bottom: 0;">Sync : {datetime.now().strftime('%H:%M')}</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

try:
    df = load_data()
    df, mois = prepare_data(df)
    df_a, df_b, df_c = separate_sections(df)
    
    # DEBUG : Afficher combien d'éléments dans chaque section
    st.write(f"DEBUG: A={len(df_a)}, B={len(df_b)}, C={len(df_c)}")
    
    # KPI GLOBAUX
    total_obj = len(df)
    total_real = len(df[df['Total'] > 0])
    taux_global = (total_real / total_obj * 100) if total_obj > 0 else 0
    total_act = int(df[mois].sum().sum())
    status_text, status_class = get_performance_status(taux_global)
    
    col1, col2, col3, col4, col5 = st.columns(5, gap="small")
    
    with col1:
        st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Objectifs</div><div class='kpi-value'>{total_obj}</div><div style='font-size: 11px; color: {COLORS['text_secondary']}; margin-top: 8px;'>Total cible</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Réalisés</div><div class='kpi-value'>{total_real}</div><div style='font-size: 11px; color: {COLORS['text_secondary']}; margin-top: 8px;'>En cours</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Taux d'exécution</div><div class='kpi-value'>{taux_global:.0f}%</div><div style='font-size: 11px; color: {COLORS['text_secondary']}; margin-top: 8px;'>Globalement</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Actions</div><div class='kpi-value'>{total_act}</div><div style='font-size: 11px; color: {COLORS['text_secondary']}; margin-top: 8px;'>Réalisées</div></div>", unsafe_allow_html=True)
    with col5:
        st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Performance</div><div class='kpi-value' style='font-size: 20px;'>✓</div><div class='badge {status_class}'>{status_text}</div></div>", unsafe_allow_html=True)
    
    # TROIS SECTIONS
    st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    # SECTION A
    with col1:
        if len(df_a) > 0:
            metrics_a = calculate_metrics(df_a, mois)
            status_a, status_cls_a = get_performance_status(metrics_a['taux'])
            st.markdown(f"""
            <div class='section-card'>
                <div style='background: linear-gradient(135deg, {COLORS['gouvernance']} 0%, {COLORS['gouvernance']} 100%); color: white; padding: 12px 16px; margin: -24px -24px 20px -24px; border-radius: 12px 12px 0 0; font-size: 16px; font-weight: 700;'>A. GOUVERNANCE</div>
                <div class='metric-row'>
                    <div class='metric-item'><div class='metric-value-small'>{metrics_a['objectifs']}</div><div class='metric-label-small'>Objectifs</div></div>
                    <div class='metric-item'><div class='metric-value-small'>{metrics_a['realises']}</div><div class='metric-label-small'>Réalisés</div></div>
                    <div class='metric-item'><div class='metric-value-small'>{metrics_a['taux']:.0f}%</div><div class='metric-label-small'>Taux</div></div>
                    <div class='metric-item'><div class='metric-value-small'>{metrics_a['actions']}</div><div class='metric-label-small'>Actions</div></div>
                </div>
                <div class='progress-bar'><div class='progress-fill' style='width: {metrics_a['taux']}%; background: {COLORS['gouvernance']};'></div></div>
                <div class='badge badge-good' style='background: #F0F9FF; color: {COLORS['gouvernance']};'>● {status_a}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # SECTION B
    with col2:
        if len(df_b) > 0:
            metrics_b = calculate_metrics(df_b, mois)
            status_b, status_cls_b = get_performance_status(metrics_b['taux'])
            st.markdown(f"""
            <div class='section-card'>
                <div style='background: linear-gradient(135deg, {COLORS['prioritaires']} 0%, {COLORS['prioritaires']} 100%); color: white; padding: 12px 16px; margin: -24px -24px 20px -24px; border-radius: 12px 12px 0 0; font-size: 16px; font-weight: 700;'>B. ACTIVITÉS PRIORITAIRES</div>
                <div class='metric-row'>
                    <div class='metric-item'><div class='metric-value-small'>{metrics_b['objectifs']}</div><div class='metric-label-small'>Objectifs</div></div>
                    <div class='metric-item'><div class='metric-value-small'>{metrics_b['realises']}</div><div class='metric-label-small'>Réalisés</div></div>
                    <div class='metric-item'><div class='metric-value-small'>{metrics_b['taux']:.0f}%</div><div class='metric-label-small'>Taux</div></div>
                    <div class='metric-item'><div class='metric-value-small'>{metrics_b['actions']}</div><div class='metric-label-small'>Actions</div></div>
                </div>
                <div class='progress-bar'><div class='progress-fill' style='width: {metrics_b['taux']}%; background: {COLORS['prioritaires']};'></div></div>
                <div class='badge badge-good' style='background: #F0F9FF; color: {COLORS['prioritaires']};'>● {status_b}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # SECTION C
    with col3:
        if len(df_c) > 0:
            metrics_c = calculate_metrics(df_c, mois)
            status_c, status_cls_c = get_performance_status(metrics_c['taux'])
            st.markdown(f"""
            <div class='section-card'>
                <div style='background: linear-gradient(135deg, {COLORS['supervision']} 0%, {COLORS['supervision']} 100%); color: white; padding: 12px 16px; margin: -24px -24px 20px -24px; border-radius: 12px 12px 0 0; font-size: 16px; font-weight: 700;'>C. AXE DE SUPERVISION</div>
                <div class='metric-row'>
                    <div class='metric-item'><div class='metric-value-small'>{metrics_c['objectifs']}</div><div class='metric-label-small'>Objectifs</div></div>
                    <div class='metric-item'><div class='metric-value-small'>{metrics_c['realises']}</div><div class='metric-label-small'>Réalisés</div></div>
                    <div class='metric-item'><div class='metric-value-small'>{metrics_c['taux']:.0f}%</div><div class='metric-label-small'>Taux</div></div>
                    <div class='metric-item'><div class='metric-value-small'>{metrics_c['actions']}</div><div class='metric-label-small'>Actions</div></div>
                </div>
                <div class='progress-bar'><div class='progress-fill' style='width: {metrics_c['taux']}%; background: {COLORS['supervision']};'></div></div>
                <div class='badge badge-good' style='background: #F0F9FF; color: {COLORS['supervision']};'>● {status_c}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # GRAPHIQUES
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: {COLORS['primary_dark']}; font-size: 18px; font-weight: 700;'>Analyses Stratégiques</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1], gap="medium")
    
    with col1:
        mois_a = [df_a[m].sum() for m in mois] if len(df_a) > 0 else [0]*6
        mois_b = [df_b[m].sum() for m in mois] if len(df_b) > 0 else [0]*6
        mois_c = [df_c[m].sum() for m in mois] if len(df_c) > 0 else [0]*6
        
        fig_ev = go.Figure()
        fig_ev.add_trace(go.Scatter(x=mois, y=mois_a, mode='lines+markers', name='Gouvernance', line=dict(color=COLORS['gouvernance'], width=3), marker=dict(size=8)))
        fig_ev.add_trace(go.Scatter(x=mois, y=mois_b, mode='lines+markers', name='Prioritaires', line=dict(color=COLORS['prioritaires'], width=3), marker=dict(size=8)))
        fig_ev.add_trace(go.Scatter(x=mois, y=mois_c, mode='lines+markers', name='Supervision', line=dict(color=COLORS['supervision'], width=3), marker=dict(size=8)))
        fig_ev.update_layout(title="<b>Évolution mensuelle des réalisations</b>", xaxis_title="Mois", yaxis_title="Actions", height=400)
        fig_ev = apply_plotly_theme(fig_ev)
        st.plotly_chart(fig_ev, use_container_width=True)
    
    with col2:
        metrics_a = calculate_metrics(df_a, mois) if len(df_a) > 0 else {'taux': 0}
        metrics_b = calculate_metrics(df_b, mois) if len(df_b) > 0 else {'taux': 0}
        metrics_c = calculate_metrics(df_c, mois) if len(df_c) > 0 else {'taux': 0}
        
        fig_perf = go.Figure()
        fig_perf.add_trace(go.Bar(y=['Gouvernance', 'Prioritaires', 'Supervision'],
            x=[metrics_a['taux'], metrics_b['taux'], metrics_c['taux']], orientation='h',
            marker=dict(color=[COLORS['gouvernance'], COLORS['prioritaires'], COLORS['supervision']]),
            text=[f"{metrics_a['taux']:.0f}%", f"{metrics_b['taux']:.0f}%", f"{metrics_c['taux']:.0f}%"],
            textposition='outside', showlegend=False))
        fig_perf.update_layout(title="<b>Performance par rubrique</b>", xaxis_title="Taux (%)", xaxis=dict(range=[0, 110]), height=350)
        fig_perf = apply_plotly_theme(fig_perf)
        st.plotly_chart(fig_perf, use_container_width=True)
    
    # TABLEAU
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: {COLORS['primary_dark']}; font-size: 18px; font-weight: 700;'>Détail des activités</h3>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Gouvernance", "Prioritaires", "Supervision"])
    
    with tab1:
        if len(df_a) > 0:
            col_liv = 'Livrable' if 'Livrable' in df_a.columns else df_a.columns[1]
            st.dataframe(df_a[[col_liv] + mois + ['Total']], use_container_width=True, hide_index=True)
        else:
            st.info("Aucune donnée pour Gouvernance")
    
    with tab2:
        if len(df_b) > 0:
            col_liv = 'Livrable' if 'Livrable' in df_b.columns else df_b.columns[1]
            st.dataframe(df_b[[col_liv] + mois + ['Total']], use_container_width=True, hide_index=True)
        else:
            st.info("Aucune donnée pour Prioritaires")
    
    with tab3:
        if len(df_c) > 0:
            col_liv = 'Livrable' if 'Livrable' in df_c.columns else df_c.columns[1]
            st.dataframe(df_c[[col_liv] + mois + ['Total']], use_container_width=True, hide_index=True)
        else:
            st.info("Aucune donnée pour Supervision")
    
    # FOOTER
    st.markdown("<div style='margin-top: 50px; padding-top: 20px; border-top: 1px solid #E2E8F0;'></div>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 11px; color: {COLORS['text_secondary']}; margin: 0;'>Dashboard DSVCo — Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y à %H:%M')}</p>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"❌ Erreur : {str(e)}")
    import traceback
    st.write(traceback.format_exc())

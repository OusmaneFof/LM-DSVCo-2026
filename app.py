import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ============================================================================
# CONFIG
# ============================================================================

st.set_page_config(
    page_title="DSVCo — Tableau de Bord S1 2026",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Couleurs institutionnelles
COLORS = {
    "primary": "#0B3A5B",
    "secondary": "#1976D2",
    "success": "#2E7D32",
    "warning": "#F57C00",
    "danger": "#D32F2F",
    "light_bg": "#F5F7FA",
    "border": "#E0E7FF",
    "text": "#1F2937",
    "text_light": "#6B7280"
}

# ============================================================================
# CHARGEMENT DONNÉES
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
    
    for col in mois:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    
    df['Total'] = df[mois].sum(axis=1)
    
    return df, mois

def classify_section(row, col_n):
    """Classifier une ligne dans A, B ou C"""
    val = str(row[col_n]).strip()
    
    # Vérifier si c'est un numéro simple (1-10) = Gouvernance
    if val.isdigit():
        if 1 <= int(val) <= 10:
            return 'A'
    
    # Vérifier si c'est B* = Supervision
    if val.upper().startswith('B'):
        return 'B'
    
    # Vérifier si c'est C* = Prioritaires
    if val.upper().startswith('C'):
        return 'C'
    
    return None

def separate_by_section(df):
    """Séparer les données par section"""
    col_n = 'N°' if 'N°' in df.columns else df.columns[0]
    
    df['Section'] = df.apply(lambda row: classify_section(row, col_n), axis=1)
    
    df_a = df[df['Section'] == 'A']
    df_b = df[df['Section'] == 'B']
    df_c = df[df['Section'] == 'C']
    
    return df_a, df_b, df_c, df[df['Section'].notna()]

def calculate_metrics(df_section, mois):
    """Calculer les métriques"""
    if len(df_section) == 0:
        return {
            'objectifs': 0,
            'realises': 0,
            'en_cours': 0,
            'non_realises': 0,
            'taux': 0.0,
            'actions': 0,
            'statut': 'N/A'
        }
    
    total_obj = len(df_section)
    total_realises = len(df_section[df_section['Total'] > 0])
    total_non_realises = total_obj - total_realises
    taux = (total_realises / total_obj * 100) if total_obj > 0 else 0
    total_actions = int(df_section[mois].sum().sum())
    
    if taux >= 80:
        statut = "Bonne performance"
    elif taux >= 50:
        statut = "À surveiller"
    else:
        statut = "Retard"
    
    return {
        'objectifs': total_obj,
        'realises': total_realises,
        'en_cours': 0,
        'non_realises': total_non_realises,
        'taux': taux,
        'actions': total_actions,
        'statut': statut
    }

def detect_attention_items(df_a, df_b, df_c):
    """Détecter les points d'attention"""
    attention = []
    
    for section_name, df_section in [("Gouvernance", df_a), ("Supervision", df_b), ("Prioritaires", df_c)]:
        col_liv = 'Livrable' if 'Livrable' in df_section.columns else df_section.columns[1] if len(df_section.columns) > 1 else 'N/A'
        
        for _, row in df_section.iterrows():
            if row['Total'] == 0:
                attention.append({
                    'livrable': row.get(col_liv, 'N/A'),
                    'section': section_name,
                    'type': 'Non réalisé',
                    'severity': 'danger'
                })
    
    return attention

# ============================================================================
# INTERFACE
# ============================================================================

def main():
    # Header
    st.markdown("## TABLEAU DE BORD DE SUIVI")
    st.markdown("**Lettre de mission 2026** • Direction de la Santé de la Ville de Conakry — DSVCo")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.caption("Période : Janvier – Juin 2026")
    with col2:
        st.caption(f"🔄 Actualisation : {datetime.now().strftime('%d %b %Y • %H:%M')}")
    
    st.divider()
    
    try:
        # Charger et préparer
        df = load_data()
        df, mois = prepare_data(df)
        df_a, df_b, df_c, df_valid = separate_by_section(df)
        
        # =====================================================================
        # KPI GLOBAUX
        # =====================================================================
        
        total_obj = len(df_valid)
        total_realises = len(df_valid[df_valid['Total'] > 0])
        total_non_realises = total_obj - total_realises
        taux_global = (total_realises / total_obj * 100) if total_obj > 0 else 0
        total_actions = int(df_valid[mois].sum().sum())
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Objectifs", total_obj, "total")
        with col2:
            st.metric("Réalisés", total_realises, f"— {total_non_realises} en attente")
        with col3:
            st.metric("Taux global", f"{taux_global:.0f}%", "exécution")
        with col4:
            st.metric("Actions", total_actions, "réalisées")
        with col5:
            perf_label = "Bonne" if taux_global >= 80 else "À surveiller" if taux_global >= 50 else "Faible"
            st.metric("Performance", perf_label, "statut")
        
        st.divider()
        
        # =====================================================================
        # TROIS AXES
        # =====================================================================
        
        st.markdown("### Performance par axe")
        
        col1, col2, col3 = st.columns(3, gap="medium")
        
        def render_axis_card(col, df_section, title, color):
            with col:
                m = calculate_metrics(df_section, mois)
                
                with st.container(border=True):
                    st.markdown(f"**{title}**")
                    
                    col_a, col_b, col_c, col_d = st.columns(4)
                    with col_a:
                        st.metric("Objectifs", m['objectifs'], label_visibility="collapsed")
                    with col_b:
                        st.metric("Réalisés", m['realises'], label_visibility="collapsed")
                    with col_c:
                        st.metric("En attente", m['non_realises'], label_visibility="collapsed")
                    with col_d:
                        st.metric("Actions", m['actions'], label_visibility="collapsed")
                    
                    # Barre de progression avec Streamlit
                    st.markdown(f"**{m['taux']:.0f}%** réalisé")
                    
                    # Créer une barre visuelle simple
                    progress_width = int(m['taux'] / 10)
                    bar = "█" * progress_width + "░" * (10 - progress_width)
                    st.markdown(f"`{bar}` {m['taux']:.0f}%")
                    
                    # Statut
                    status_color = "🟢" if m['taux'] >= 80 else "🟠" if m['taux'] >= 50 else "🔴"
                    st.markdown(f"{status_color} {m['statut']}")
        
        render_axis_card(col1, df_a, "A. GOUVERNANCE", "#1565C0")
        render_axis_card(col2, df_b, "B. AXE DE SUPERVISION", "#EF6C00")
        render_axis_card(col3, df_c, "C. ACTIVITÉS PRIORITAIRES", "#2E7D32")
        
        st.divider()
        
        # =====================================================================
        # ANALYSE
        # =====================================================================
        
        st.markdown("### Analyse de la performance")
        
        col1, col2 = st.columns(2, gap="medium")
        
        # Comparaison des taux
        with col1:
            m_a = calculate_metrics(df_a, mois)
            m_b = calculate_metrics(df_b, mois)
            m_c = calculate_metrics(df_c, mois)
            
            fig_comparison = go.Figure()
            fig_comparison.add_trace(go.Bar(
                y=['Gouvernance', 'Supervision', 'Prioritaires'],
                x=[m_a['taux'], m_b['taux'], m_c['taux']],
                orientation='h',

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

st.set_page_config(page_title="Tableau de Bord DSVCo S1 2026", layout="wide")
st.title("📊 Tableau de Bord DSVCo S1 2026")
st.write("Suivi Interactif des Performances - Semestre 1 2026")

uploaded_file = st.file_uploader("Téléchargez votre fichier de suivi", type=['xlsx', 'xls'])

if uploaded_file:
    try:
        # Lire les sheets
        df_activites = pd.read_excel(uploaded_file, sheet_name='Tableau de bord S1')
        df_calendrier = pd.read_excel(uploaded_file, sheet_name='Calendrier Échéances S1')
        df_suivi = pd.read_excel(uploaded_file, sheet_name='Suivi Mensuel S1')
        
        st.success("✅ Fichier chargé avec succès !")
        
        # SECTION 1 : MÉTRIQUES CLÉS
        st.subheader("📈 Indicateurs Clés")
        
        # Calculer le taux de réalisation
        try:
            df_suivi_clean = df_suivi.iloc[2:14].copy()
            df_suivi_clean.columns = ['N°', 'Livrable', 'Cible', 'Cumul', 'Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Réalisation']
            
            # Convertir les colonnes en numérique
            for col in ['Cumul', 'Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin']:
                df_suivi_clean[col] = pd.to_numeric(df_suivi_clean[col], errors='coerce').fillna(0)
            
            cumul_total = df_suivi_clean['Cumul'].sum()
            cible_total = df_suivi_clean['Cible'].sum()
            taux_realisation = (cumul_total / cible_total * 100) if cible_total > 0 else 0
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("📊 Cible S1", f"{int(cible_total)}", "livrables")
            col2.metric("✅ Réalisé", f"{int(cumul_total)}", "livrables")
            col3.metric("📈 Taux Réalisation", f"{taux_realisation:.1f}%")
            col4.metric("⏳ Échéances", f"{len(df_calendrier.iloc[2:15])}", "prévues")
        except:
            st.warning("Erreur lors du calcul des métriques")
        
        # SECTION 2 : GRAPHIQUES
        st.divider()
        st.subheader("📊 Analyses Détaillées")
        
        col1, col2 = st.columns(2)
        
        # Graphique 1 : Suivi mensuel
        with col1:
            try:
                mois = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin']
                valeurs = [df_suivi_clean[m].sum() for m in mois]
                
                fig1 = go.Figure()
                fig1.add_trace(go.Bar(
                    x=mois,
                    y=valeurs,
                    marker=dict(color='#1f77b4'),
                    name='Réalisations'
                ))
                fig1.update_layout(
                    title="Progression Mensuelle des Livrables",
                    xaxis_title="Mois",
                    yaxis_title="Nombre de livrables",
                    height=400,
                    template='plotly_white'
                )
                st.plotly_chart(fig1, use_container_width=True)
            except:
                st.error("Erreur graphique 1")
        
        # Graphique 2 : Réalisation par livrable
        with col2:
            try:
                fig2 = go.Figure()
                fig2.add_trace(go.Bar(
                    y=df_suivi_clean['Livrable'].head(10),
                    x=df_suivi_clean['Cumul'].head(10),
                    orientation='h',
                    marker=dict(color='#2ca02c'),
                    name='Réalisé'
                ))
                fig2.update_layout(
                    title="Top 10 Livrables Réalisés",
                    xaxis_title="Nombre",
                    height=400,
                    template='plotly_white'
                )
                st.plotly_chart(fig2, use_container_width=True)
            except:
                st.error("Erreur graphique 2")
        
        col1, col2 = st.columns(2)
        
        # Graphique 3 : Jauge de réalisation
        with col1:
            fig3 = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=taux_realisation,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Taux Réalisation Global"},
                delta={'reference': 50},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#1f77b4"},
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
            fig3.update_layout(height=400)
            st.plotly_chart(fig3, use_container_width=True)
        
        # Graphique 4 : Statut des échéances
        with col2:
            try:
                df_cal_clean = df_calendrier.iloc[2:15].copy()
                statuts = df_cal_clean.iloc[:, 4].value_counts()
                
                fig4 = go.Figure(data=[go.Pie(
                    labels=statuts.index,
                    values=statuts.values,
                    marker=dict(colors=['#ff7f0e', '#2ca02c', '#d62728']),
                    textinfo='label+percent'
                )])
                fig4.update_layout(
                    title="Statut des Échéances S1",
                    height=400
                )
                st.plotly_chart(fig4, use_container_width=True)
            except:
                st.warning("Graphique statut non disponible")
        
        # SECTION 3 : TABLEAU CALENDRIER
        st.divider()
        st.subheader("📅 Calendrier des Échéances")
        
        try:
            df_cal_display = df_calendrier.iloc[2:15].copy()
            df_cal_display.columns = ['Mois', 'Échéance', 'Livrable', 'Responsable', 'Statut', 'Observations']
            st.dataframe(df_cal_display, use_container_width=True, hide_index=True)
        except:
            st.error("Impossible d'afficher le calendrier")
        
        # SECTION 4 : TABLEAU SUIVI
        st.divider()
        st.subheader("📋 Suivi des Livrables")
        
        try:
            st.dataframe(df_suivi_clean, use_container_width=True, hide_index=True)
        except:
            st.error("Impossible d'afficher le suivi")
        
    except Exception as e:
        st.error(f"❌ Erreur : {str(e)}")
        st.info("Assurez-vous que le fichier contient les sheets : 'Tableau de bord S1', 'Calendrier Échéances S1', 'Suivi Mensuel S1'")

else:
    st.info("👈 Téléchargez votre fichier Tableau_de_Bord_DSVCo_S1_2026_OF.xlsx")

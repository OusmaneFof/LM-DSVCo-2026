import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Tableau de Bord DSVCo S1 2026", layout="wide")
st.title("📊 Tableau de Bord DSVCo S1 2026")
st.write("Surveillance Sanitaire - Guinée")

uploaded_file = st.file_uploader("Téléchargez votre fichier DHIS2", type=['xls', 'xlsx'])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, sheet_name=0)
        df.columns = df.iloc[0]
        df = df.iloc[1:].reset_index(drop=True)
        
        df_simple = pd.DataFrame({
            'Établissement': df.iloc[:, 1],
            'Paludisme': pd.to_numeric(df.iloc[:, 3], errors='coerce'),
            'Testés': pd.to_numeric(df.iloc[:, 5], errors='coerce'),
            'Ebola': pd.to_numeric(df.iloc[:, 19], errors='coerce'),
            'Lassa': pd.to_numeric(df.iloc[:, 25], errors='coerce'),
            'Choléra': pd.to_numeric(df.iloc[:, 55], errors='coerce'),
            'Décès': pd.to_numeric(df.iloc[:, 9], errors='coerce')
        })
        
        df_simple = df_simple.fillna(0)
        
        total_palu = int(df_simple['Paludisme'].sum())
        total_ebola = int(df_simple['Ebola'].sum())
        total_lassa = int(df_simple['Lassa'].sum())
        total_cholera = int(df_simple['Choléra'].sum())
        total_deces = int(df_simple['Décès'].sum())
        
        st.success("✅ Fichier chargé avec succès !")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("📊 Paludisme", f"{total_palu:,}")
        col2.metric("⚠️ Ebola", total_ebola)
        col3.metric("Lassa", total_lassa)
        col4.metric("Choléra", total_cholera)
        col5.metric("💀 Décès", total_deces)
        
        st.divider()
        st.subheader("📈 Graphiques Interactifs")
        
        col1, col2 = st.columns(2)
        
        with col1:
            top15 = df_simple.nlargest(15, 'Paludisme')
            fig1 = go.Figure()
            fig1.add_trace(go.Bar(
                x=top15['Paludisme'],
                y=top15['Établissement'],
                orientation='h',
                marker=dict(color='#d62728'),
                name='Cas'
            ))
            fig1.update_layout(
                title="Top 15 Établissements - Paludisme",
                xaxis_title="Nombre de cas",
                yaxis_title="Établissement",
                height=500,
                template='plotly_white'
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            maladies = ['Paludisme', 'Ebola', 'Lassa', 'Choléra']
            values = [total_palu, total_ebola, total_lassa, total_cholera]
            colors = ['#ff7f0e', '#e74c3c', '#9b59b6', '#3498db']
            fig2 = go.Figure(data=[go.Pie(
                labels=maladies,
                values=values,
                marker=dict(colors=colors),
                textinfo='label+percent'
            )])
            fig2.update_layout(
                title="Distribution des Maladies",
                height=500,
                template='plotly_white'
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            top10_test = df_simple.nlargest(10, 'Testés')
            if len(top10_test) > 0:
                taux = (top10_test['Paludisme'] / (top10_test['Testés'] + 1) * 100).values
                etab_short = [e[:20] + "..." if len(str(e)) > 20 else str(e) for e in top10_test['Établissement'].values]
                fig3 = go.Figure()
                fig3.add_trace(go.Scatter(
                    x=etab_short,
                    y=taux,
                    mode='lines+markers',
                    name='Taux (%)',
                    line=dict(color='#1f77b4', width=3),
                    marker=dict(size=10)
                ))
                fig3.update_layout(
                    title="Taux de Positivité Paludisme",
                    yaxis_title="Taux (%)",
                    height=400,
                    template='plotly_white'
                )
                st.plotly_chart(fig3, use_container_width=True)
        
        with col2:
            fig4 = go.Figure()
            fig4.add_trace(go.Bar(
                x=['Ebola', 'Lassa', 'Choléra'],
                y=[total_ebola, total_lassa, total_cholera],
                marker=dict(color=['#e74c3c', '#9b59b6', '#3498db']),
                name='Cas'
            ))
            fig4.update_layout(
                title="Maladies Graves",
                yaxis_title="Nombre de cas",
                height=400,
                template='plotly_white'
            )
            st.plotly_chart(fig4, use_container_width=True)
        
        st.divider()
        st.subheader("📋 Données Brutes")
        st.dataframe(df_simple.head(20), use_container_width=True)
        
    except Exception as e:
        st.error(f"❌ Erreur : {str(e)}")

else:
    st.info("👈 Téléchargez un fichier DHIS2 pour voir le dashboard")

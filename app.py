import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import networkx as nx
import matplotlib.pyplot as plt
from src.data_loader import BinanceDataLoader
from src.models.dcc_garch import DCCGARCH
from src.models.backtest import run_hedging_backtest
from src.network.graph_utils import build_mst_network

# --- CONFIGURATION ---
st.set_page_config(page_title="Crypto Risk 2026", layout="wide")

st.title("🛡️ Crypto Systemic Risk Monitor")

# Initialisation de l'état
if 'analysed' not in st.session_state:
    st.session_state.analysed = False

# --- FONCTIONS CACHÉES (Cœur de l'optimisation) ---
@st.cache_data
def run_heavy_calculations(assets, start_date_str):
    """
    Télécharge et calcule le modèle DCC-GARCH. 
    Cette fonction est mise en mémoire (cachée) pour ne pas être relancée
    lorsque vous bougez seulement le curseur du seuil.
    """
    loader = BinanceDataLoader()
    data = loader.get_crypto_dataset(assets, start_date_str)
    
    # Calcul des rendements (scaled pour GARCH)
    returns = np.log(data / data.shift(1)).dropna() * 100
    
    # Modèle DCC-GARCH
    dcc = DCCGARCH(returns)
    dcc_corr, _ = dcc.calculate_dynamic_correlation()
    sys_index = dcc.get_systemic_index(dcc_corr)
    
    return returns, sys_index

# --- SIDEBAR ---
st.sidebar.header("🕹️ Configuration")
assets = st.sidebar.multiselect(
    "Actifs", 
    ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "FTT/USDT"],
    default=["BTC/USDT", "ETH/USDT", "SOL/USDT"]
)
start_date = st.sidebar.date_input("Depuis le", pd.to_datetime("2023-01-01"))

# Ce curseur peut maintenant être bougé sans relancer les calculs GARCH
risk_threshold = st.sidebar.slider("Seuil d'alerte (Contagion)", 0.0, 1.0, 0.7)

if st.sidebar.button("🚀 Lancer l'Analyse"):
    st.session_state.analysed = True

# --- LOGIQUE PRINCIPALE ---
if st.session_state.analysed:
    try:
        # 1. Calculs lourds (ou récupération du cache)
        # On utilise start_date.strftime pour le cache car l'objet date n'est pas hashable
        returns, sys_index = run_heavy_calculations(assets, start_date.strftime('%Y-%m-%d'))

        # --- AFFICHAGE ---
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("📈 Indice de Risque Systémique")
            df_plot = sys_index.to_frame(name="Corrélation").astype(float)
            
            fig_idx = px.line(df_plot, title="Saturation de la Contagion")
            
            # --- AJOUT DU SEUIL DYNAMIQUE ---
            fig_idx.add_hline(
                y=risk_threshold, 
                line_dash="dash", 
                line_color="red", 
                annotation_text=f"Seuil Alerte: {risk_threshold:.2f}",
                annotation_position="top left"
            )
            
            st.plotly_chart(fig_idx, width='stretch')

        with col2:
            st.subheader("🕸️ Topologie (MST)")
            # MST basé sur les corrélations statiques globales
            mst_graph = build_mst_network(returns.corr())
            fig_net, ax = plt.subplots(figsize=(6, 4), facecolor='#0e1117')
            pos = nx.spring_layout(mst_graph)
            nx.draw(mst_graph, pos, with_labels=True, node_color='#00d4ff', 
                    edge_color='white', font_color='white', node_size=1000, ax=ax)
            st.pyplot(fig_net)

        st.divider()

        st.subheader("🚀 Backtest de Couverture")
        # Le backtest réagit instantanément au changement de seuil
        results = run_hedging_backtest(returns / 100, sys_index, threshold=risk_threshold)
        
        # Comparaison visuelle de l'efficacité du seuil choisi
        fig_bt = px.line(results.astype(float), title=f"Performance vs Benchmark (Seuil: {risk_threshold})")
        st.plotly_chart(fig_bt, width='stretch')

    except Exception as e:
        st.error(f"Erreur lors de l'analyse : {e}")
        st.session_state.analysed = False
else:
    st.info("Sélectionnez vos actifs et cliquez sur 'Lancer l'Analyse' pour démarrer.")
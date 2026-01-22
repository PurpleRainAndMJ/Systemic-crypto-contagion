import yaml
import pandas as pd
from src.data_loader import BinanceDataLoader
from src.data_processing import compute_log_returns
from src.models.dcc_garch import DCCGARCH
from src.network.graph_utils import build_mst_network
from src.visualization import plot_rolling_correlation, plot_network

def main():
    # 1. Chargement de la configuration
    with open("config/settings.yaml", "r") as f:
        config = yaml.safe_load(f)

    # 2. Récupération des données
    loader = BinanceDataLoader()
    symbols = config['assets']['majors'] + config['assets']['crisis_triggers']
    raw_data = loader.get_risk_assets_dataset(symbols, config['analysis']['start_date'])
    
    # 3. Calcul des rendements
    returns = compute_log_returns(raw_data)
    
    # 4. Modélisation DCC-GARCH
    print("📈 Estimation du modèle DCC-GARCH...")
    dcc_model = DCCGARCH(returns)
    dcc_corr, vols = dcc_model.calculate_dynamic_correlation()
    sys_index = dcc_model.get_systemic_index(dcc_corr)
    
    # 5. Analyse de Réseau (sur la période de crise FTX par exemple)
    print("🕸️ Analyse du réseau de contagion...")
    crisis_date = config['events']['ftx_collapse']
    # Corrélation statique autour de la crise pour le graphe
    correlation_matrix = returns.loc['2022-11-01':'2022-11-15'].corr()
    mst_graph = build_mst_network(correlation_matrix)
    
    # 6. Visualisations
    print("📊 Génération des graphiques...")
    # Corrélation moyenne du marché
    plot_rolling_correlation(sys_index, "Indice Systémique Global")
    # Graphe de réseau
    plot_network(mst_graph)

if __name__ == "__main__":
    main()
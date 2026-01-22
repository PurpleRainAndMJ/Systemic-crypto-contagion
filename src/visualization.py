import seaborn as sns
import matplotlib.pyplot as plt

def plot_rolling_correlation(rolling_corr, asset_name):
    """Affiche l'explosion des corrélations pendant les crises (ex: FTX)"""
    plt.figure(figsize=(12, 6))
    plt.plot(rolling_corr)
    plt.title(f"Corrélation glissante (60j) : {asset_name} vs Marché")
    plt.axhline(y=rolling_corr.mean(), color='r', linestyle='--', label='Moyenne')
    plt.fill_between(rolling_corr.index, 0.8, 1, where=(rolling_corr > 0.8), 
                     color='red', alpha=0.3, label='Zone de Contagion')
    plt.legend()
    plt.show()

def plot_network(graph):
    """Visualise le réseau de dépendance entre actifs"""
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=2000, 
            node_color="skyblue", font_size=10, font_weight="bold")
    plt.title("Arbre Couvrant Minimal des Dépendances Crypto")
    plt.show()
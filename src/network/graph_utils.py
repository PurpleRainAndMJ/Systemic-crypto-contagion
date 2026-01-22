import networkx as nx
import numpy as np

def build_mst_network(correlation_matrix):
    """Construit un Minimum Spanning Tree (MST) à partir des corrélations"""
    # Transformation Corrélation -> Distance
    distance_matrix = np.sqrt(2 * (1 - correlation_matrix.clip(-1, 1)))
    
    # Création du graphe complet
    G = nx.from_pandas_adjacency(distance_matrix)
    
    # Extraction de l'arbre couvrant minimal (MST)
    # Cela réduit le bruit et garde les liens de contagion les plus forts
    mst = nx.minimum_spanning_tree(G)
    return mst

def get_centrality_metrics(graph):
    """Identifie les actifs 'hubs' (sources de risque systémique)"""
    return nx.degree_centrality(graph)
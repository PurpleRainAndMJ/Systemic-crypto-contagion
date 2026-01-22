from src.network.graph_utils import build_mst_network
import networkx as nx

def test_mst_properties(sample_returns):
    corr_matrix = sample_returns.corr()
    mst = build_mst_network(corr_matrix)
    
    # Un MST pour 3 actifs doit avoir exactement 2 arêtes
    assert len(mst.edges()) == len(sample_returns.columns) - 1
    # Le graphe doit être connexe (tous les actifs sont reliés)
    assert nx.is_connected(mst)
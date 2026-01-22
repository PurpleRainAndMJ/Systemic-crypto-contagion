import numpy as np
from src.data_processing import compute_log_returns

def test_compute_log_returns(sample_prices):
    returns = compute_log_returns(sample_prices)
    
    # Vérification de la dimension (N-1)
    assert len(returns) == len(sample_prices) - 1
    
    # Vérification manuelle du premier log-return : ln(21000/20000)
    expected = np.log(21000 / 20000)
    assert np.isclose(returns.iloc[0]['BTC'], expected)
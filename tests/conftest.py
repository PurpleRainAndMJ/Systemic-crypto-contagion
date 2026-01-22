import pytest
import pandas as pd
import numpy as np

@pytest.fixture
def sample_returns():
    """Génère 100 jours de rendements fictifs pour 3 actifs"""
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', periods=100)
    data = np.random.normal(0, 0.02, (100, 3))
    df = pd.DataFrame(data, index=dates, columns=['BTC', 'ETH', 'SOL'])
    return df

@pytest.fixture
def sample_prices():
    """Génère des prix fictifs"""
    dates = pd.date_range('2023-01-01', periods=10)
    prices = pd.DataFrame({'BTC': [20000, 21000, 20500, 22000, 21500, 23000, 22500, 24000, 23500, 25000]}, index=dates)
    return prices
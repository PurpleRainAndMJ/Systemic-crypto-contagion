import pandas as pd
from src.models.backtest import run_hedging_backtest

def test_hedging_logic(sample_returns):
    # On simule un indice de risque très élevé (1.0 partout)
    high_risk_index = pd.Series([1.0] * len(sample_returns), index=sample_returns.index)
    
    # Seuil à 0.5 (donc l'alerte est toujours activée)
    results = run_hedging_backtest(sample_returns, high_risk_index, threshold=0.5)
    
    # La stratégie active ne doit pas bouger (rendement 0 -> prix stable à 1.0)
    # Note : Le premier jour peut être investi selon la logique du shift()
    assert results['Strategie_Active'].iloc[-1] == results['Strategie_Active'].iloc[1]
import pandas as pd

def run_hedging_backtest(returns, systemic_index, threshold=0.7):
    """
    Si l'indice systémique > seuil, on sort du marché (rendement 0 = USDT).
    """
    # Rendement moyen du panier d'actifs (Equally Weighted)
    market_returns = returns.mean(axis=1)
    
    # Signal : 1 si on reste investi, 0 si on sort en USDT
    signal = (systemic_index < threshold).shift(1).fillna(1)
    
    active_returns = market_returns * signal
    
    return pd.DataFrame({
        'Panier_Passif': (1 + market_returns).cumprod(),
        'Strategie_Active': (1 + active_returns).cumprod()
    })
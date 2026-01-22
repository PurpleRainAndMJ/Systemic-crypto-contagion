import numpy as np
from scipy.stats import norm

def calculate_var(returns, confidence_level=0.95):
    """Value-at-Risk historique simple"""
    return np.percentile(returns, (1 - confidence_level) * 100)

def calculate_covar(asset_returns, market_returns, confidence_level=0.95):
    """
    Approche simplifiée par régression quantile pour la CoVaR.
    Note : Pour un profil expert, utilisez 'statsmodels.regression.quantile_regression'.
    """
    # Ici, une version simplifiée basée sur la corrélation
    correlation = asset_returns.corr(market_returns)
    var_asset = calculate_var(asset_returns, confidence_level)
    
    # CoVaR estimée par la sensibilité (Beta) au risque de l'actif
    beta_spread = correlation * (market_returns.std() / asset_returns.std())
    covar = beta_spread * var_asset
    return covar
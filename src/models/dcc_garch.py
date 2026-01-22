import numpy as np
import pandas as pd
from arch import arch_model

class DCCGARCH:
    def __init__(self, returns):
        self.returns = returns
        self.assets = returns.columns
        self.num_assets = len(self.assets)

    def estimate_univariate_garch(self):
        """Étape 1 : Estimer les modèles GARCH(1,1) pour chaque actif"""
        residuals = []
        volatilities = []
        
        for asset in self.assets:
            model = arch_model(self.returns[asset], vol='Garch', p=1, q=1, dist='normal')
            res = model.fit(disp='off')
            # Standardisation des résidus
            volatilities.append(res.conditional_volatility)
            residuals.append(res.resid / res.conditional_volatility)
            
        return pd.DataFrame(residuals).T, pd.DataFrame(volatilities).T

    def calculate_dynamic_correlation(self):
        """Étape 2 : Calculer la corrélation dynamique simplifiée (Rolling DCC)"""
        # Pour un projet Master/Pro, une fenêtre glissante sur les résidus standardisés
        # est une approximation robuste de la matrice Q de Engle.
        std_residuals, vols = self.estimate_univariate_garch()
        dcc_corr = std_residuals.rolling(window=30).corr()
        
        return dcc_corr, vols

    def get_systemic_index(self, dcc_corr):
        """Calcule la corrélation moyenne du système (Indicateur de stress)"""
        # Moyenne des corrélations hors diagonale
        avg_corr = dcc_corr.groupby(level=0).apply(lambda x: x.values[np.triu_indices(self.num_assets, k=1)].mean())
        return avg_corr
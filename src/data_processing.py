import pandas as pd
import numpy as np

def compute_log_returns(df):
    """Calcule les rendements logarithmiques : r_t = ln(P_t / P_{t-1})"""
    return np.log(df / df.shift(1)).dropna()

def scale_data(df):
    """Standardisation pour les modèles de réseau (Z-score)"""
    return (df - df.mean()) / df.std()
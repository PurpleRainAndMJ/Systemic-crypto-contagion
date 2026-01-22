# 🛡️ Systemic-Crypto-Contagion (Binance-Only Edition)

Analyse quantitative de la propagation des risques au sein de l'écosystème Binance. 

## 📊 Résumé du Projet
Ce projet utilise les données de l'API Binance pour modéliser la **contagion endogène**. L'objectif est de démontrer comment, lors de crises comme **FTX** ou **Luna**, les corrélations internes du marché crypto saturent, rendant toute diversification entre altcoins inutile.

## 🛠️ Stack Technique
- **Data** : Binance API via `ccxt`.
- **Modélisation** : DCC-GARCH pour les corrélations dynamiques.
- **Réseau** : Théorie des graphes (MST) pour cartographier les liens de dépendance.
- **Dashboard** : Interface interactive avec `Streamlit`.
- **Qualité** : Logging industriel et tests unitaires avec `pytest`.

## 📈 Stratégie de Gestion des Risques
Le projet inclut un module de **Backtesting** qui simule une sortie du marché (vers l'USDT) lorsque l'indice systémique dépasse un seuil de saturation critique.

## 🚦 Installation et Usage
1. `pip install -r requirements.txt`
2. `streamlit run app.py`
3. Lancer les tests : `pytest tests/`
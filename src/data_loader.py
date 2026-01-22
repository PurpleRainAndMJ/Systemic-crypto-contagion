import ccxt
import pandas as pd
import time
from datetime import datetime

class BinanceDataLoader:
    def __init__(self):
        self.exchange = ccxt.binance({
            'enableRateLimit': True,  # Respecter les limites de l'API
        })

    def fetch_crypto_data(self, symbol, start_date, timeframe='1d'):
        """
        Récupère les données historiques pour un symbole donné.
        Format date : '2022-01-01'
        """
        since = self.exchange.parse8601(f"{start_date}T00:00:00Z")
        all_ohlcv = []
        
        print(f"📥 Téléchargement de {symbol}...")
        
        while since < self.exchange.milliseconds():
            try:
                # Récupération par paquets de 1000 bougies
                ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, since)
                if not ohlcv:
                    break
                
                since = ohlcv[-1][0] + 1
                all_ohlcv += ohlcv
                
                # Petit délai pour la sécurité
                time.sleep(self.exchange.rateLimit / 1000)
                
            except Exception as e:
                print(f"Erreur sur {symbol}: {e}")
                break

        # Conversion en DataFrame
        df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        
        return df['close'] # On ne garde que le prix de clôture pour les corrélations

    def get_risk_assets_dataset(self, symbols, start_date):
        """
        Récupère plusieurs actifs et les combine dans un seul DataFrame.
        """
        dataset = pd.DataFrame()
        
        for s in symbols:
            series = self.fetch_crypto_data(s, start_date)
            dataset[s.replace('/USDT', '')] = series
            
        return dataset

# --- EXEMPLE D'UTILISATION ---
if __name__ == "__main__":
    loader = BinanceDataLoader()
    
    # Actifs pour l'étude de contagion
    # Note : LUNA (ancien) est souvent listé comme LUNC ou a été delisté de certains spots.
    assets = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'FTT/USDT'] 
    
    data = loader.get_risk_assets_dataset(assets, '2022-01-01')
    
    # Sauvegarde dans le dossier data/raw
    data.to_csv('data/raw/crypto_prices.csv')
    print("✅ Données sauvegardées dans data/raw/crypto_prices.csv")
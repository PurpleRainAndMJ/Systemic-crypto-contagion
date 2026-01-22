import ccxt
import pandas as pd
import time
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BinanceDataLoader:
    def __init__(self):
        self.exchange = ccxt.binance({'enableRateLimit': True})

    def fetch_crypto_data(self, symbol, start_date):
        logging.info(f"📥 Récupération des données Binance pour {symbol}...")
        since = self.exchange.parse8601(f"{start_date}T00:00:00Z")
        all_ohlcv = []
        
        while since < self.exchange.milliseconds():
            try:
                ohlcv = self.exchange.fetch_ohlcv(symbol, '1d', since)
                if not ohlcv: break
                since = ohlcv[-1][0] + 1
                all_ohlcv += ohlcv
                time.sleep(self.exchange.rateLimit / 1000)
            except Exception as e:
                logging.error(f"Erreur sur {symbol}: {e}")
                break

        df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df.set_index('timestamp')['close']

    def get_crypto_dataset(self, symbols, start_date):
        dataset = pd.DataFrame()
        for s in symbols:
            dataset[s.split('/')[0]] = self.fetch_crypto_data(s, start_date)
        return dataset.dropna()
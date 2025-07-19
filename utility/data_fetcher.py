import pandas as pd
import ccxt  # Or your preferred exchange library
from typing import Optional

class DataFetcher:
    def __init__(self, config):
        self.exchange = ccxt.binance({  # Example with Binance
            'apiKey': config['exchange']['api_key'],
            'secret': config['exchange']['api_secret']
        })
        self.symbols = config['trading']['symbols']
        self.timeframe = config['trading']['timeframe']
        
    def get_data(self, symbol: str, timeframe: str, limit: int = 100) -> Optional[pd.DataFrame]:
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            return df
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None

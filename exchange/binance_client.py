import ccxt
import pandas as pd
from typing import Optional, Dict, List
import time
from datetime import datetime

class BinanceClient:
    def __init__(self, api_key: str, api_secret: str):
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future'  # or 'spot' depending on your account
            }
        })
        
    def get_ohlcv(self, symbol: str, timeframe: str = '5m', limit: int = 100) -> Optional[pd.DataFrame]:
        """Get OHLCV data from Binance"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            return df
        except Exception as e:
            print(f"Error fetching OHLCV for {symbol}: {e}")
            return None

    def get_account_balance(self) -> Dict:
        """Get account balance"""
        try:
            balance = self.exchange.fetch_balance()
            return {k: v for k, v in balance['total'].items() if float(v) > 0}
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return {}

    def create_order(self, symbol: str, side: str, quantity: float, 
                    price: Optional[float] = None, stop_loss: Optional[float] = None,
                    take_profit: Optional[float] = None) -> Dict:
        """Create an order with optional stop loss and take profit"""
        try:
            # Main order
            order_type = 'limit' if price else 'market'
            order_params = {
                'symbol': symbol,
                'side': side,
                'type': order_type,
                'quantity': quantity,
            }
            if price:
                order_params['price'] = price

            # Place the order
            order = self.exchange.create_order(**order_params)
            
            # OCO order for SL/TP (Binance Spot only)
            if stop_loss and take_profit:
                self.exchange.create_order(
                    symbol=symbol,
                    side='SELL' if side == 'BUY' else 'BUY',
                    type='STOP_LOSS_LIMIT',
                    quantity=quantity,
                    stopPrice=stop_loss,
                    price=stop_loss,
                    params={'stopLossPrice': stop_loss, 'takeProfitPrice': take_profit}
                )
            
            return order
        except Exception as e:
            print(f"Error creating order: {e}")
            return {}

    def test_connection(self) -> bool:
        """Test if connection to Binance works"""
        try:
            self.exchange.fetch_time()
            return True
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False

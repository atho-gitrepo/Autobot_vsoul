import requests
from typing import Dict
import yaml
import os

class TelegramNotifier:
    def __init__(self):
        with open(os.path.join('config', 'secrets.yaml')) as f:
            secrets = yaml.safe_load(f)
        self.token = secrets['telegram']['bot_token']
        self.chat_id = secrets['telegram']['chat_id']
    
    def send_signal(self, signal: Dict, symbol: str, timeframe: str):
        emoji = "🟢" if signal['type'] == 'BUY' else "🔴"
        message = (
            f"{emoji} *{signal['type']} Signal* {emoji}\n\n"
            f"*Symbol:* {symbol}\n"
            f"*Timeframe:* {timeframe}\n"
            f"*Entry:* `{signal['entry']:.4f}`\n"
            f"*SL:* `{signal['stop_loss']:.4f}` | *TP:* `{signal['take_profit']:.4f}`\n"
            f"*Risk:* {signal['risk_factor']}x | TDI: `{signal['tdi_value']:.2f}`\n"
            f"*Time:* {signal['time']}\n\n"
            f"*Conditions Met:*\n"
            f"- TDI in {'Hard' if signal['risk_factor'] == 2 else 'Soft'} {signal['type']} Zone\n"
            f"- Price rejected {'lower' if signal['type'] == 'BUY' else 'upper'} BB\n"
            f"- MA crossover confirmed\n"
        )
        
        self._send_message(message)
    
    def _send_message(self, text: str):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {
            'chat_id': self.chat_id,
            'text': text,
            'parse_mode': 'Markdown'
        }
        requests.post(url, params=params)

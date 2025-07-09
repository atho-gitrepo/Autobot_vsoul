# Binance Trading Bot with Super TDI & Bollinger Bands Strategy

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Telegram](https://img.shields.io/badge/Telegram-Notifier-blue)

A Python trading bot that implements the Consolidated Trend Trading Strategy using Super TDI and Super Bollinger Bands indicators, with Binance API integration and Telegram notifications.

## 📌 Features

- **Advanced Technical Indicators**:
  - Super Traders Dynamic Index (TDI) with RSI-based zones
  - Enhanced Bollinger Bands with volatility detection
- **Smart Signal Detection**:
  - Hard/Soft Buy/Sell zones
  - Trend confirmation with MA crossovers
  - Bollinger Band rejection patterns
- **Exchange Integration**:
  - Real-time data from Binance (Spot/Futures)
  - Order execution with risk management
- **Notifications**:
  - Telegram alerts with detailed trade information
  - Risk factor indicators (1x/2x)
- **Risk Management**:
  - Configurable position sizing
  - Automatic stop-loss/take-profit levels

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/binance-trading-bot.git
   cd binance-trading-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up configuration:
   ```bash
   cp config/config.example.yaml config/config.yaml
   cp config/secrets.example.yaml config/secrets.yaml
   ```

## ⚙️ Configuration

Edit the configuration files:

### `config/config.yaml`
```yaml
trading:
  symbols: ["BTCUSDT", "ETHUSDT"]  # Trading pairs
  timeframe: "5m"                  # Chart timeframe
  risk_per_trade: 0.5              # Risk % per trade
  execute_trades: false            # Enable live trading

strategy:
  tdi:
    rsi_period: 10
    hard_buy_zone: 25
    soft_buy_zone: 35
    no_trade_zone: [45, 55]
    soft_sell_zone: 65
    hard_sell_zone: 75
```

### `config/secrets.yaml`
```yaml
binance:
  api_key: "your_api_key"
  api_secret: "your_api_secret"

telegram:
  bot_token: "your_bot_token"
  chat_id: "your_chat_id"
```

## 🚀 Usage

Run the bot:
```bash
python main.py
```

### Command Line Options
```bash
python main.py --debug      # Enable debug mode
python main.py --testnet    # Use Binance testnet
```

## 📊 Strategy Logic

### Buy Signal Conditions
1. TDI enters Buyer Zone (<50 or rejecting 35/25)
2. Green line crosses above Red line in TDI
3. Price touches lower Bollinger Band with rejection
4. Confirmed when price reverses inside BB

### Sell Signal Conditions
1. TDI enters Seller Zone (>50 or rejecting 65/75)
2. Green line crosses below Red line in TDI
3. Price touches upper Bollinger Band with rejection
4. Confirmed when price reverses inside BB

## 📈 Sample Telegram Alert

```
🚀 BUY Signal 🚀

Symbol: BTCUSDT
Timeframe: 5m
Entry Price: 42356.25
Stop Loss: 42120.50
Take Profit: 42780.75
Risk Factor: 2x (Hard Buy)
TDI Value: 23.45

Conditions Met:
- TDI in Hard Buy Zone (below 25)
- Price rejected lower Bollinger Band
- MA crossover confirmed
- Volume increasing on reversal
```

## 📂 Project Structure

```
binance-trading-bot/
├── config/               # Configuration files
├── exchange/             # Binance API integration
├── indicators/           # Technical indicators
├── strategies/           # Trading strategies
├── notifications/        # Telegram notification system
├── tests/                # Unit tests
├── main.py               # Main application
└── README.md
```

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ Risk Disclaimer

This software is for educational purposes only. Do not risk money which you are afraid to lose. USE THIS SOFTWARE AT YOUR OWN RISK. THE DEVELOPERS ASSUME NO RESPONSIBILITY FOR YOUR TRADING RESULTS.

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

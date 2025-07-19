# Trading Bot System Architecture

## Overview

This is an algorithmic trading bot system built in Python that implements the Consolidated Trend Trading Strategy using enhanced Super TDI and Super Bollinger indicators. The system features zone-based signal detection, rejection pattern analysis, and risk-factor based position sizing with comprehensive Telegram notifications.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The trading bot follows a modular, event-driven architecture with the following key layers:

### Core Architecture Components

1. **Main Orchestrator** (`main.py`): Coordinates all components and runs the main trading loop
2. **Configuration Layer** (`config/settings.py`): Centralized configuration management with dataclasses
3. **Data Layer** (`src/data/`): Handles market data collection and storage
4. **Indicators Layer** (`src/indicators/`): Technical analysis indicators (TDI and Bollinger Bands)
5. **Strategy Layer** (`src/strategy/`): Trading strategy that combines multiple indicators
6. **Backtesting Engine** (`src/backtest/`): Strategy testing and performance evaluation
7. **Notifications Layer** (`src/notifications/`): Alert system via Telegram
8. **Utilities Layer** (`src/utils/`): Logging and helper functions

## Key Components

### Data Management
- **DataCollector**: Fetches real-time market data from external APIs (primarily Binance)
- **DataStorage**: SQLite-based storage for market data and trading signals with async operations
- Uses aiohttp for async HTTP requests and aiosqlite for async database operations

### Technical Indicators
- **SuperTDI**: Enhanced with zone-based detection (Hard/Soft Buy/Sell zones), MA crossover detection, and risk factor calculation
  - Hard Buy Zone: RSI ≤ 25 (2x risk factor)
  - Soft Buy Zone: RSI ≤ 35 (1x risk factor)
  - No Trade Zone: RSI 45-55
  - Soft Sell Zone: RSI ≥ 65 (1x risk factor)
  - Hard Sell Zone: RSI ≥ 75 (2x risk factor)
- **SuperBollinger**: Advanced with rejection pattern detection, reversal confirmation, and band touch analysis
  - Detects price rejection at band levels
  - Confirms reversals inside bands
  - Enhanced squeeze and expansion detection
- Both indicators provide comprehensive signal structures with confidence levels and pattern confirmation

### Trading Strategy
- **ConsolidatedTrendStrategy**: Enhanced zone-based strategy implementing specific buy/sell conditions:
  - **Buy Conditions**: TDI in buyer zones + Green line crosses above Red line + Bollinger rejection patterns
  - **Sell Conditions**: TDI in seller zones + Green line crosses below Red line + Bollinger rejection patterns
  - **Risk Management**: Zone-based position sizing (2x for hard zones, 1x for soft zones)
  - **Signal Confirmation**: Requires MA crossovers, BB rejections, and volume confirmation

### Backtesting System
- **Backtester**: Comprehensive backtesting engine with performance metrics
- **Trade**: Individual trade tracking with P&L calculation
- **BacktestResults**: Detailed performance statistics and analysis

### Notification System
- **TelegramNotifier**: Enhanced with detailed signal information matching professional trading format
- Includes TDI zone information, risk factors (1x/2x), and condition confirmation
- Real-time alerts with entry price, stop loss, take profit, and strategy details
- Rate limiting and message queuing to prevent spam

## Data Flow

1. **Data Collection**: DataCollector fetches OHLCV data from external APIs
2. **Data Storage**: Market data is stored in SQLite database via DataStorage
3. **Indicator Calculation**: SuperTDI and SuperBollinger process the market data
4. **Signal Generation**: ConsolidatedStrategy combines indicator signals
5. **Risk Management**: Strategy applies position sizing and risk controls
6. **Notification**: TelegramNotifier sends alerts for significant signals
7. **Backtesting**: Historical data flows through the same pipeline for strategy validation

## External Dependencies

### APIs and Data Sources
- **Binance API**: Primary source for cryptocurrency market data
- **Telegram Bot API**: For sending trading notifications and alerts

### Python Libraries
- **aiohttp**: Async HTTP client for API requests
- **aiosqlite**: Async SQLite database operations
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations for indicators
- **pytest**: Testing framework

### Database
- **SQLite**: Local database for storing market data and trading history
- Uses WAL mode for better concurrency with async operations

## Deployment Strategy

### Local Development
- Python 3.7+ environment with async/await support
- SQLite database stored locally in `data/` directory
- Configuration via YAML files and environment variables
- Comprehensive logging to files in `logs/` directory

### Configuration Management
- Dataclass-based configuration system
- Support for multiple environments (development, production)
- External configuration files for sensitive data (API keys, tokens)

### Testing Strategy
- Unit tests for all major components
- Mock-based testing for external API dependencies
- Backtesting framework for strategy validation
- Test data generation for reproducible testing

### Monitoring and Logging
- Structured JSON logging with multiple output formats
- Log rotation and retention policies
- Performance metrics and error tracking
- Real-time notifications via Telegram

### Security Considerations
- API keys and tokens stored in environment variables
- Rate limiting for external API calls
- Input validation for all external data
- Error handling and graceful degradation

## Recent Changes (July 2025)

- **Enhanced TDI Zones**: Implemented hard/soft buy/sell zones with risk factor calculation
- **Bollinger Rejection Patterns**: Added detection for price rejection at band levels with reversal confirmation
- **Zone-Based Strategy Logic**: Updated strategy to match specific buy/sell conditions from trading requirements
- **Professional Telegram Notifications**: Enhanced message format with zone information, risk factors, and condition details
- **Risk Management**: Integrated zone-based position sizing and risk factor multipliers

The system is designed to be easily extensible with new indicators, strategies, and data sources while maintaining clean separation of concerns and robust error handling.
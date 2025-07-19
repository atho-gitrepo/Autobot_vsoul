#!/usr/bin/env python3
"""
Algorithmic Trading Bot - Main Entry Point
Coordinates all components and runs the trading bot with signal generation.
"""

import asyncio
import logging
import signal
import sys
from datetime import datetime, timedelta
from typing import Optional

from config.settings import Settings
from src.data.data_collector import DataCollector
from src.data.data_storage import DataStorage
from src.indicators.super_tdi import SuperTDI
from src.indicators.super_bollinger import SuperBollinger
from src.strategy.consolidated_strategy import ConsolidatedStrategy
from src.notifications.telegram_bot import TelegramNotifier
from src.utils.logger import setup_logger


class TradingBot:
    """Main trading bot orchestrator."""
    
    def __init__(self):
        self.settings = Settings()
        self.logger = setup_logger('trading_bot', self.settings.log_level)
        
        # Initialize components
        self.data_collector = DataCollector(self.settings)
        self.data_storage = DataStorage(self.settings)
        self.telegram_notifier = TelegramNotifier(self.settings)
        
        # Initialize indicators
        self.super_tdi = SuperTDI(self.settings.tdi_config)
        self.super_bollinger = SuperBollinger(self.settings.bollinger_config)
        
        # Initialize strategy
        self.strategy = ConsolidatedStrategy(
            self.super_tdi, 
            self.super_bollinger, 
            self.settings.strategy_config
        )
        
        self.running = False
        
    async def initialize(self):
        """Initialize all components."""
        try:
            self.logger.info("Initializing trading bot...")
            
            # Initialize data storage
            await self.data_storage.initialize()
            
            # Initialize Telegram bot
            await self.telegram_notifier.initialize()
            
            # Send startup notification
            await self.telegram_notifier.send_message(
                f"🤖 Trading Bot Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            
            self.logger.info("Trading bot initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize trading bot: {e}")
            raise
    
    async def collect_and_analyze_data(self, symbol: str):
        """Collect data and generate trading signals."""
        try:
            # Collect latest market data
            data = await self.data_collector.get_market_data(
                symbol, 
                self.settings.data_config['timeframe'],
                self.settings.data_config['lookback_periods']
            )
            
            if data is None or len(data) < self.settings.strategy_config['min_data_points']:
                self.logger.warning(f"Insufficient data for {symbol}")
                return
            
            # Store data
            await self.data_storage.store_market_data(symbol, data)
            
            # Calculate indicators
            tdi_signals = self.super_tdi.calculate(data)
            bollinger_signals = self.super_bollinger.calculate(data)
            
            # Generate strategy signals
            strategy_signal = self.strategy.generate_signal(
                data, tdi_signals, bollinger_signals
            )
            
            if strategy_signal:
                await self.handle_signal(symbol, strategy_signal, data)
                
        except Exception as e:
            self.logger.error(f"Error processing data for {symbol}: {e}")
            await self.telegram_notifier.send_message(
                f"❌ Error processing {symbol}: {str(e)}"
            )
    
    async def handle_signal(self, symbol: str, signal: dict, data):
        """Handle generated trading signals."""
        try:
            current_price = data['close'].iloc[-1]
            timestamp = data.index[-1]
            
            # Log signal
            self.logger.info(
                f"Signal generated for {symbol}: {signal['action']} at {current_price}"
            )
            
            # Store signal
            await self.data_storage.store_signal(symbol, signal, timestamp)
            
            # Send Telegram notification
            await self.send_signal_notification(symbol, signal, current_price, timestamp)
            
        except Exception as e:
            self.logger.error(f"Error handling signal for {symbol}: {e}")
    
    async def send_signal_notification(self, symbol: str, signal: dict, price: float, timestamp):
        """Send signal notification via Telegram."""
        try:
            action_emoji = "🟢" if signal['action'] == 'BUY' else "🔴" if signal['action'] == 'SELL' else "🟡"
            
            message = f"""
{action_emoji} **{signal['action']} SIGNAL**
📊 Symbol: {symbol}
💰 Price: ${price:.4f}
⏰ Time: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
🎯 Confidence: {signal['confidence']:.2f}%
📈 Strategy: {signal['strategy_name']}

**Indicator Analysis:**
• TDI: {signal.get('tdi_signal', 'N/A')}
• Bollinger: {signal.get('bollinger_signal', 'N/A')}

**Risk Management:**
• Stop Loss: ${signal.get('stop_loss', 'N/A')}
• Take Profit: ${signal.get('take_profit', 'N/A')}
            """
            
            await self.telegram_notifier.send_message(message.strip())
            
        except Exception as e:
            self.logger.error(f"Error sending notification: {e}")
    
    async def run_analysis_cycle(self):
        """Run a single analysis cycle for all configured symbols."""
        for symbol in self.settings.trading_config['symbols']:
            await self.collect_and_analyze_data(symbol)
            await asyncio.sleep(1)  # Small delay between symbols
    
    async def run(self):
        """Main trading bot loop."""
        self.running = True
        self.logger.info("Starting trading bot main loop...")
        
        try:
            while self.running:
                start_time = datetime.now()
                
                await self.run_analysis_cycle()
                
                # Calculate next run time
                cycle_duration = (datetime.now() - start_time).total_seconds()
                sleep_time = max(0, self.settings.trading_config['analysis_interval'] - cycle_duration)
                
                if sleep_time > 0:
                    self.logger.debug(f"Cycle completed in {cycle_duration:.2f}s, sleeping for {sleep_time:.2f}s")
                    await asyncio.sleep(sleep_time)
                else:
                    self.logger.warning(f"Cycle took {cycle_duration:.2f}s, longer than interval!")
                    
        except Exception as e:
            self.logger.error(f"Error in main loop: {e}")
            await self.telegram_notifier.send_message(f"❌ Trading bot error: {str(e)}")
            raise
    
    async def shutdown(self):
        """Graceful shutdown of the trading bot."""
        self.logger.info("Shutting down trading bot...")
        self.running = False
        
        try:
            await self.telegram_notifier.send_message(
                f"🛑 Trading Bot Stopped at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            await self.telegram_notifier.shutdown()
            await self.data_storage.close()
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")


async def main():
    """Main entry point."""
    bot = None
    
    def signal_handler(signum, frame):
        print(f"\nReceived signal {signum}, shutting down...")
        if bot:
            asyncio.create_task(bot.shutdown())
        sys.exit(0)
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        bot = TradingBot()
        await bot.initialize()
        await bot.run()
        
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, shutting down...")
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        sys.exit(1)
    finally:
        if bot:
            await bot.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

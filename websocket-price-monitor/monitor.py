import json
import asyncio
import websockets
import config
from notifier import TelegramNotifier

class BybitWSMonitor:
    """
    Subscribes to Bybit public Spot trades via WebSockets and monitors
    price changes in real time.
    """
    def __init__(self, symbol: str = "BTCUSDT"):
        self.symbol = symbol.upper()
        self.ws_url = "wss://stream.bybit.com/v5/public/spot"
        self.notifier = TelegramNotifier()
        self.last_price = None
        self.reference_price = None
        self.threshold = config.PRICE_CHANGE_THRESHOLD_PERCENT
        self.is_running = False

    async def connect_and_listen(self):
        """
        Main socket loop. Keeps connection alive, reconnects automatically on failure,
        and processes incoming frame updates.
        """
        self.is_running = True
        print(f"Connecting to Bybit WebSocket for {self.symbol}...")
        
        while self.is_running:
            try:
                async with websockets.connect(self.ws_url, ping_interval=20, ping_timeout=10) as ws:
                    print("WebSocket connection established.")
                    
                    # Send subscription payload
                    sub_message = {
                        "op": "subscribe",
                        "args": [f"publicTrade.{self.symbol}"]
                    }
                    await ws.send(json.dumps(sub_message))
                    print(f"Subscribed to publicTrade.{self.symbol}")
                    
                    async for message in ws:
                        data = json.loads(message)
                        
                        # Verify subscription response or actual trade data
                        if "topic" in data and f"publicTrade.{self.symbol}" in data["topic"]:
                            await self.process_trades(data["data"])
                            
            except websockets.exceptions.ConnectionClosed as e:
                print(f"WebSocket connection closed ({e}). Reconnecting in 5 seconds...")
                await asyncio.sleep(5)
            except Exception as e:
                print(f"WebSocket error: {e}. Reconnecting in 5 seconds...")
                await asyncio.sleep(5)

    async def process_trades(self, trades_list: list):
        """Parses price info from the trade updates and calculates price movements."""
        for trade in trades_list:
            price = float(trade["p"]) # 'p' contains price in Bybit's V5 schema
            
            # Initial setup of prices
            if self.last_price is None:
                self.last_price = price
                self.reference_price = price
                print(f"Initial {self.symbol} price set to: {price:.2f} USDT")
                continue

            self.last_price = price
            
            # Compute percentage change from reference price
            change_percent = ((price - self.reference_price) / self.reference_price) * 100
            
            # Trigger alert if change exceeds threshold (either up or down)
            if abs(change_percent) >= self.threshold:
                print(f"[ALERT TRIGGERED] {self.symbol} moved {change_percent:+.3f}% (New: {price:.2f}, Ref: {self.reference_price:.2f})")
                
                # Send alert asynchronously
                asyncio.create_task(
                    self.notifier.send_alert(self.symbol, self.reference_price, price, change_percent)
                )
                
                # Set new reference price to avoid duplicate alerts for the same spike
                self.reference_price = price
            else:
                # Log micro movements to console for debugging/demo visual
                print(f"[{self.symbol}] Price updated: {price:.2f} USDT (Move: {change_percent:+.3f}%)")

    def stop(self):
        """Gracefully stops the monitor connection."""
        self.is_running = False

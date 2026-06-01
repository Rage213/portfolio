import asyncio
import sys
from monitor import BybitWSMonitor

async def main():
    # Setup monitoring for BTCUSDT (default)
    symbol = "BTCUSDT"
    if len(sys.argv) > 1:
        symbol = sys.argv[1].upper()

    monitor = BybitWSMonitor(symbol=symbol)
    
    print("=" * 60)
    print(f"Starting Nexus Labs Real-Time WebSocket Monitor for {symbol}")
    print(f"Alert threshold is configured to {monitor.threshold}%")
    print("=" * 60)
    
    try:
        await monitor.connect_and_listen()
    except KeyboardInterrupt:
        print("\nStopping WebSocket monitor gracefully...")
        monitor.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProcess terminated by user.")

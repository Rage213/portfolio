import aiohttp
import asyncio
import config

class TelegramNotifier:
    """
    Asynchronously sends real-time price alerts to Telegram.
    """
    def __init__(self):
        self.bot_token = config.TELEGRAM_BOT_TOKEN
        self.chat_id = config.TELEGRAM_CHAT_ID
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    async def send_alert(self, symbol: str, old_price: float, new_price: float, change: float):
        """
        Sends an alert message to Telegram about price threshold breaches.
        """
        direction = "📈 ВЗЛЕТЕЛА" if change > 0 else "📉 УПАЛА"
        percent_str = f"{change:+.3f}%"
        
        message = (
            f"⚠️ **REAL-TIME ALERT: {symbol}**\n\n"
            f"Цена актива {direction} на **{percent_str}**!\n"
            f"Предыдущая цена: `{old_price:.2f} USDT`\n"
            f"Текущая цена: `{new_price:.2f} USDT`\n\n"
            f"⚡ _Мониторинг осуществляется Nexus Labs WebSocket Engine._"
        )

        # Skip API call if we're using default mock token
        if "MOCK" in self.bot_token:
            print(f"[Notifier MOCK Alert] {symbol} {direction} by {percent_str} (Old: {old_price:.2f}, New: {new_price:.2f})")
            return

        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "chat_id": self.chat_id,
                    "text": message,
                    "parse_mode": "Markdown"
                }
                async with session.post(self.api_url, json=payload, timeout=5) as response:
                    if response.status == 200:
                        print(f"[{symbol}] Alert sent successfully to Telegram.")
                    else:
                        resp_text = await response.text()
                        print(f"[{symbol}] Failed to send alert: {response.status} - {resp_text}")
        except Exception as e:
            print(f"[{symbol}] Notification error: {e}")

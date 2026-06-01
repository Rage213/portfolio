import aiohttp
from typing import Dict, Any, Optional
import logging
from config import CRYPTO_PAY_TOKEN

logger = logging.getLogger("crypto-client")

class CryptoPayClient:
    def __init__(self, token: str, testnet: bool = True):
        self.token = token
        self.base_url = "https://testnet-pay.cryptomus.com/api/v1" if testnet else "https://pay.cryptomus.com/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    async def create_invoice(self, amount: float, currency: str = "USDT", description: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Создает инвойс на оплату в Crypto Bot / Cryptomus API"""
        url = f"{self.base_url}/payment"
        payload = {
            "amount": str(amount),
            "currency": currency,
            "order_id": f"order_{description}", # В реальном API здесь передается уникальный ID заказа
        }
        
        # Для демонстрации без реального токена возвращаем мок-объект
        if "mock" in self.token:
            import uuid
            mock_id = str(uuid.uuid4())
            return {
                "result": {
                    "uuid": mock_id,
                    "url": f"https://t.me/CryptoBot?start={mock_id}",
                    "amount": amount,
                    "status": "active"
                }
            }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload, headers=self.headers) as response:
                    if response.status == 200:
                        return await response.json()
                    logger.error(f"Error creating invoice: {response.status} {await response.text()}")
                    return None
            except Exception as e:
                logger.error(f"Request failed: {e}")
                return None

    async def get_invoice(self, uuid: str) -> Optional[Dict[str, Any]]:
        """Проверяет статус созданного инвойса"""
        url = f"{self.base_url}/payment/info"
        payload = {"uuid": uuid}

        if "mock" in self.token:
            return {
                "result": {
                    "uuid": uuid,
                    "status": "paid"  # Имитируем успешную оплату при проверке
                }
            }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload, headers=self.headers) as response:
                    if response.status == 200:
                        return await response.json()
                    return None
            except Exception as e:
                logger.error(f"Check invoice failed: {e}")
                return None

crypto_pay = CryptoPayClient(CRYPTO_PAY_TOKEN)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Dict, Any

def get_start_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🛍️ Каталог товаров", callback_data="catalog")],
        [InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_catalog_keyboard(products: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
    buttons = []
    for product in products:
        buttons.append([InlineKeyboardButton(
            text=f"{product['name']} — ${product['price_usd']}",
            callback_data=f"buy_{product['id']}"
        )])
    buttons.append([InlineKeyboardButton(text="🔙 Главное меню", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_payment_keyboard(pay_url: str, invoice_id: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="💳 Оплатить", url=pay_url)],
        [InlineKeyboardButton(text="🔄 Проверить оплату", callback_data=f"check_{invoice_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

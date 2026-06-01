from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_user_menu() -> InlineKeyboardMarkup:
    """Returns main user catalog and order menu."""
    buttons = [
        [
            InlineKeyboardButton(text="🛍️ Купить Скрипт (990 руб.)", callback_data="buy_script"),
            InlineKeyboardButton(text="🤖 Купить Бот (2490 руб.)", callback_data="buy_bot")
        ],
        [
            InlineKeyboardButton(text="📞 Поддержка", url="https://t.me/knrcharge")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_admin_menu() -> InlineKeyboardMarkup:
    """Returns admin control panel menu."""
    buttons = [
        [
            InlineKeyboardButton(text="📊 Показать Аналитику (График)", callback_data="admin_stats"),
            InlineKeyboardButton(text="✉️ Сделать Рассылку", callback_data="admin_broadcast")
        ],
        [
            InlineKeyboardButton(text="👥 Кол-во пользователей", callback_data="admin_users_count")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

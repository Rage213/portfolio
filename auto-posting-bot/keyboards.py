from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Dict, Any

def get_main_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="📝 Создать отложенный пост", callback_data="create_post")],
        [InlineKeyboardButton(text="📢 Добавить канал", callback_data="add_channel")],
        [InlineKeyboardButton(text="📋 Список запланированных", callback_data="list_scheduled")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_channels_keyboard(channels: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
    buttons = []
    for channel in channels:
        buttons.append([InlineKeyboardButton(
            text=channel["title"],
            callback_data=f"select_channel_{channel['channel_id']}"
        )])
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_cancel_keyboard() -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_action")]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

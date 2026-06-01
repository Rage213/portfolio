from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_captcha_keyboard(user_id: int) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="✅ Я не робот", callback_data=f"verify_{user_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

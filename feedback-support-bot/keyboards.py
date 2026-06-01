from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_user_menu() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="✍️ Написать обращение", callback_data="create_ticket")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_admin_ticket_keyboard(ticket_id: int) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="💬 Ответить", callback_data=f"reply_ticket_{ticket_id}"),
            InlineKeyboardButton(text="✅ Закрыть", callback_data=f"resolve_ticket_{ticket_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_cancel_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_action")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

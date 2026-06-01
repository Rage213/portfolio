from aiogram import Router, F
from aiogram.types import Message
from collections import defaultdict
import time
import re
from config import SPAM_THRESHOLD

router = Router()

# Буфер времени последних сообщений для антифлуда: user_id -> list of timestamps
user_messages = defaultdict(list)

# Список запрещенных паттернов (ссылки, реклама казино, скам каналы)
SPAM_REGEX = re.compile(
    r"(t\.me/joinchat|t\.me/\+|bit\.ly|v\.to/|cutt\.ly|крипта|заработок|казино|slots|casino|выигрыш)",
    re.IGNORECASE
)

def is_flood(user_id: int) -> bool:
    """Определяет флуд: более SPAM_THRESHOLD сообщений за последние 5 секунд"""
    now = time.time()
    user_messages[user_id] = [t for t in user_messages[user_id] if now - t < 5]
    user_messages[user_id].append(now)
    return len(user_messages[user_id]) > SPAM_THRESHOLD

@router.message(F.chat.type.in_(["group", "supergroup"]))
async def filter_messages(message: Message):
    # Игнорируем сообщения от администраторов
    member = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if member.status in ["administrator", "creator"]:
        return

    # 1. Проверка на флуд
    if is_flood(message.from_user.id):
        try:
            await message.delete()
            # Дополнительно ограничиваем пользователя на отправку сообщений (мут на 5 минут)
            from datetime import datetime, timedelta
            from aiogram.types import ChatPermissions
            until_date = datetime.now() + timedelta(minutes=5)
            await message.chat.restrict(
                user_id=message.from_user.id,
                permissions=ChatPermissions(can_send_messages=False),
                until_date=until_date
            )
            await message.answer(f"⚠️ Пользователь **{message.from_user.full_name}** временно заблокирован на 5 минут за флуд.", parse_mode="Markdown")
        except Exception:
            pass
        return

    # 2. Проверка на спам-ссылки / ключевые слова
    text = message.text or message.caption or ""
    if SPAM_REGEX.search(text):
        try:
            await message.delete()
            # Предупреждение пользователю
            await message.answer(f"🚫 Сообщение пользователя **{message.from_user.full_name}** удалено за рекламу / спам-ссылку.", parse_mode="Markdown")
        except Exception:
            pass

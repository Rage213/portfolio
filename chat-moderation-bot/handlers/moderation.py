from aiogram import Router, F
from aiogram.types import Message, ChatPermissions
from aiogram.filters import Command
from datetime import datetime
import database
from filters import IsAdminFilter
from utils import parse_time

router = Router()
router.message.filter(IsAdminFilter())

@router.message(Command("ban"))
async def cmd_ban(message: Message):
    if not message.reply_to_message:
        await message.answer("Эта команда должна быть ответом на сообщение нарушителя!")
        return

    target_user = message.reply_to_message.from_user
    reason = message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else "Не указана"

    try:
        await message.chat.ban(user_id=target_user.id)
        await message.answer(
            f"👤 Пользователь **{target_user.full_name}** ({target_user.id}) был забанен.\n📝 **Причина:** {reason}",
            parse_mode="Markdown"
        )
    except Exception as e:
        await message.answer(f"Не удалось забанить пользователя. Ошибка: {e}")

@router.message(Command("mute"))
async def cmd_mute(message: Message):
    if not message.reply_to_message:
        await message.answer("Эта команда должна быть ответом на сообщение!")
        return

    target_user = message.reply_to_message.from_user
    args = message.text.split()
    
    time_limit = "1h"
    reason = "Не указана"
    
    if len(args) > 1:
        time_limit = args[1]
    if len(args) > 2:
        reason = " ".join(args[2:])

    duration = parse_time(time_limit)
    if not duration:
        await message.answer("Неверный формат времени! Используйте, например: `10m`, `2h`, `1d`.", parse_mode="Markdown")
        return

    until_date = datetime.now() + duration
    permissions = ChatPermissions(can_send_messages=False, can_send_media_messages=False)

    try:
        await message.chat.restrict(
            user_id=target_user.id,
            permissions=permissions,
            until_date=until_date
        )
        await message.answer(
            f"🔇 Пользователь **{target_user.full_name}** переведен в режим только чтение до {until_date.strftime('%Y-%m-%d %H:%M:%S')}.\n"
            f"📝 **Причина:** {reason}",
            parse_mode="Markdown"
        )
    except Exception as e:
        await message.answer(f"Не удалось выдать мут. Ошибка: {e}")

@router.message(Command("warn"))
async def cmd_warn(message: Message):
    if not message.reply_to_message:
        await message.answer("Эта команда должна быть ответом на сообщение!")
        return

    target_user = message.reply_to_message.from_user
    reason = message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else "Не указана"

    # Добавляем варн в БД
    warn_count = await database.add_warning(target_user.id, message.chat.id, reason)
    
    await message.answer(
        f"⚠️ Пользователь **{target_user.full_name}** получил предупреждение ({warn_count}/3).\n"
        f"📝 **Причина:** {reason}",
        parse_mode="Markdown"
    )

    if warn_count >= 3:
        # Автоматический бан при 3 варнах
        try:
            await message.chat.ban(user_id=target_user.id)
            await database.reset_warnings(target_user.id, message.chat.id)
            await message.answer(f"🚫 Пользователь **{target_user.full_name}** автоматически забанен за достижение 3 предупреждений.", parse_mode="Markdown")
        except Exception as e:
            await message.answer(f"Не удалось автоматически забанить пользователя: {e}")

@router.message(Command("unwarn"))
async def cmd_unwarn(message: Message):
    if not message.reply_to_message:
        await message.answer("Эта команда должна быть ответом на сообщение!")
        return

    target_user = message.reply_to_message.from_user
    await database.reset_warnings(target_user.id, message.chat.id)
    await message.answer(f"✅ Все предупреждения пользователя **{target_user.full_name}** сброшены.", parse_mode="Markdown")

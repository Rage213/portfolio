from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ChatPermissions
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION
from aiogram.types import ChatMemberUpdated
import keyboards
import asyncio

router = Router()

# Список пользователей, проходящих капчу: user_id -> welcome_msg_id
pending_users = {}

@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def on_user_join(event: ChatMemberUpdated):
    user = event.new_chat_member.user
    chat = event.chat

    # Ограничиваем нового пользователя сразу (запрещаем писать сообщения)
    try:
        await chat.restrict(
            user_id=user.id,
            permissions=ChatPermissions(can_send_messages=False)
        )
    except Exception:
        pass

    # Отправляем сообщение-капчу
    msg = await event.bot.send_message(
        chat_id=chat.id,
        text=f"👋 Добро пожаловать, **{user.full_name}**!\n\n"
             "Чтобы получить доступ к чату, подтвердите, что вы человек, нажав кнопку ниже.",
        reply_markup=keyboards.get_captcha_keyboard(user.id),
        parse_mode="Markdown"
    )
    
    pending_users[user.id] = msg.message_id

    # Запускаем фоновую таску на автокик через 60 секунд, если капча не решена
    async def auto_kick_timer(user_id, chat_id, message_id):
        await asyncio.sleep(60)
        if user_id in pending_users and pending_users[user_id] == message_id:
            try:
                await event.bot.ban_chat_member(chat_id=chat_id, user_id=user_id)
                await event.bot.unban_chat_member(chat_id=chat_id, user_id=user_id) # Разбаниваем, чтобы мог войти снова потом
                await event.bot.delete_message(chat_id=chat_id, message_id=message_id)
            except Exception:
                pass
            pending_users.pop(user_id, None)

    asyncio.create_task(auto_kick_timer(user.id, chat.id, msg.message_id))

@router.callback_query(F.data.startswith("verify_"))
async def process_captcha_verification(call: CallbackQuery):
    target_user_id = int(call.data.split("_")[1])
    
    if call.from_user.id != target_user_id:
        await call.answer("Это подтверждение не для вас!", show_alert=True)
        return

    # Возвращаем права пользователю
    try:
        await call.message.chat.restrict(
            user_id=call.from_user.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        
        await call.answer("Проверка пройдена! Добро пожаловать.", show_alert=True)
        await call.message.delete()
    except Exception as e:
        await call.answer(f"Не удалось выдать права: {e}", show_alert=True)

    pending_users.pop(call.from_user.id, None)

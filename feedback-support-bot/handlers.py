from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_ID
import database
import keyboards

router = Router()

class UserStates(StatesGroup):
    waiting_for_ticket = State()

class AdminStates(StatesGroup):
    waiting_for_reply = State()

def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID

# --- Обработчики Пользователя ---

@router.message(Command("start"))
async def cmd_start(message: Message):
    await database.add_user(message.from_user.id, message.from_user.username)
    if is_admin(message.from_user.id):
        try:
            await message.answer(
                "👑 Добро пожаловать в панель администратора бота поддержки!\n\n"
                "Сюда будут поступать все заявки от пользователей. Вы можете отвечать на них напрямую, используя функцию реплая (ответ на сообщение), либо кликнув по кнопке под заявкой."
            )
        except Exception as e:
            print(f"Ошибка ответа админу в cmd_start: {e}")
    else:
        try:
            await message.answer(
                f"👋 Привет, {message.from_user.full_name}!\n\n"
                "Это официальный бот обратной связи. Нажмите кнопку ниже, чтобы отправить ваше обращение или задать вопрос администратору.",
                reply_markup=keyboards.get_user_menu()
            )
        except Exception as e:
            print(f"Ошибка ответа пользователю в cmd_start: {e}")

@router.callback_query(F.data == "create_ticket")
async def start_create_ticket(call: CallbackQuery, state: FSMContext):
    try:
        await call.message.edit_text(
            "📝 Введите текст вашего обращения. Постарайтесь описать задачу или вопрос как можно подробнее:",
            reply_markup=keyboards.get_cancel_keyboard()
        )
    except Exception as e:
        print(f"Ошибка изменения сообщения в start_create_ticket: {e}")
    await state.set_state(UserStates.waiting_for_ticket)

@router.callback_query(F.data == "cancel_action")
async def process_cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    if is_admin(call.from_user.id):
        await call.message.edit_text("Действие отменено.")
    else:
        await call.message.edit_text(
            "Отправка отменена. Вы можете создать обращение в любое время.",
            reply_markup=keyboards.get_user_menu()
        )

@router.message(UserStates.waiting_for_ticket)
async def process_ticket_text(message: Message, state: FSMContext):
    ticket_text = message.text
    if not ticket_text:
        await message.answer("Пожалуйста, отправьте текстовое сообщение:")
        return

    # Сохраняем в БД
    ticket_id = await database.create_ticket(message.from_user.id, ticket_text)
    await state.clear()
    
    # Отправляем подтверждение пользователю
    try:
        await message.answer("✅ Ваше обращение успешно отправлено! Ожидайте ответа администратора.")
    except Exception as e:
        print(f"Не удалось отправить подтверждение пользователю: {e}")

    # Пересылаем заявку админу
    username_info = f" (@{message.from_user.username})" if message.from_user.username else ""
    admin_msg_text = (
        f"📥 **Новая заявка #{ticket_id}**\n\n"
        f"👤 **Отправитель:** {message.from_user.full_name}{username_info}\n"
        f"🆔 **ID:** `{message.from_user.id}`\n\n"
        f"💬 **Текст обращения:**\n{ticket_text}"
    )
    
    try:
        sent_msg = await message.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_msg_text,
            reply_markup=keyboards.get_admin_ticket_keyboard(ticket_id),
            parse_mode="Markdown"
        )
        # Связываем ID сообщения админа с тикетом для автореплая по переписке
        await database.update_ticket_admin_msg(ticket_id, sent_msg.message_id)
    except Exception as e:
        print(f"Ошибка отправки уведомления админу: {e}")


# --- Обработчики Администратора ---

# 1. Автореплай на обычные Telegram-ответы (нативное цитирование)
@router.message(F.chat.id == ADMIN_ID, F.reply_to_message)
async def process_admin_native_reply(message: Message):
    # Ищем тикет, связанный с сообщением, на которое ответил админ
    ticket = await database.get_ticket_by_admin_msg(message.reply_to_message.message_id)
    if not ticket:
        return # Если это реплай не на карточку тикета, игнорируем
        
    reply_text = message.text
    if not reply_text:
        await message.answer("Пожалуйста, отправьте текстовый ответ.")
        return

    try:
        # Отправляем ответ пользователю
        await message.bot.send_message(
            chat_id=ticket["user_id"],
            text=f"✉️ **Ответ администратора на вашу заявку:**\n\n{reply_text}",
            parse_mode="Markdown"
        )
        await database.close_ticket(ticket["id"])
        await message.answer(f"✅ Ответ на заявку #{ticket['id']} успешно доставлен пользователю. Заявка закрыта.")
    except Exception as e:
        await message.answer(f"❌ Не удалось доставить ответ пользователю. Возможно, бот заблокирован.\n\nОшибка: {e}")

# 2. Кнопка "Ответить" под тикетом
@router.callback_query(F.data.startswith("reply_ticket_"))
async def start_reply_ticket(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        return
        
    ticket_id = int(call.data.split("_")[2])
    await call.message.reply(
        f"✍️ Введите ответ на заявку #{ticket_id}:",
        reply_markup=keyboards.get_cancel_keyboard()
    )
    await state.update_data(reply_ticket_id=ticket_id)
    await state.set_state(AdminStates.waiting_for_reply)

# Обработка ввода ответа через стейт
@router.message(AdminStates.waiting_for_reply)
async def process_admin_state_reply(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
        
    data = await state.get_data()
    ticket_id = data.get("reply_ticket_id")
    
    # Загружаем инфо о тикете по ID
    ticket = await database.get_ticket(ticket_id)

    if not ticket:
        await message.answer("Заявка не найдена.")
        await state.clear()
        return

    reply_text = message.text
    try:
        await message.bot.send_message(
            chat_id=ticket["user_id"],
            text=f"✉️ **Ответ администратора на вашу заявку:**\n\n{reply_text}",
            parse_mode="Markdown"
        )
        await database.close_ticket(ticket_id)
        await state.clear()
        await message.answer(f"✅ Ответ на заявку #{ticket_id} успешно отправлен. Заявка закрыта.")
    except Exception as e:
        await message.answer(f"❌ Не удалось отправить ответ: {e}")
        await state.clear()

# 3. Кнопка "Закрыть" тикет без ответа
@router.callback_query(F.data.startswith("resolve_ticket_"))
async def resolve_ticket(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return
        
    ticket_id = int(call.data.split("_")[2])
    await database.close_ticket(ticket_id)
    await call.answer("Обращение помечено как закрытое.", show_alert=True)
    await call.message.edit_reply_markup(reply_markup=None) # Убираем кнопки

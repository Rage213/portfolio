from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
import re

import database
import keyboards
from scheduler import schedule_post
from config import ADMIN_IDS

router = Router()

class PostStates(StatesGroup):
    channel = State()
    content = State()
    time = State()

class ChannelStates(StatesGroup):
    add = State()

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

@router.message(Command("start"))
async def cmd_start(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Доступ запрещен.")
        return
    await message.answer(
        "👋 Добро пожаловать в панель управления отложенным постингом.\n\n"
        "Выберите действие ниже:",
        reply_markup=keyboards.get_main_keyboard()
    )

@router.callback_query(F.data == "back_to_main")
@router.callback_query(F.data == "cancel_action")
async def process_back_to_main(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        "Панель управления отложенным постингом.\n\n"
        "Выберите действие ниже:",
        reply_markup=keyboards.get_main_keyboard()
    )

# --- Добавление канала ---
@router.callback_query(F.data == "add_channel")
async def start_add_channel(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        "Чтобы добавить канал, следуйте инструкции:\n\n"
        "1. Добавьте этого бота в ваш канал в качестве администратора с правами публикации.\n"
        "2. Перешлите любое сообщение из канала в этот чат или введите ID канала:",
        reply_markup=keyboards.get_cancel_keyboard()
    )
    await state.set_state(ChannelStates.add)

@router.message(ChannelStates.add)
async def process_channel_id(message: Message, state: FSMContext):
    channel_id = None
    title = "Канал"
    username = None

    if message.forward_from_chat:
        channel_id = message.forward_from_chat.id
        title = message.forward_from_chat.title
        username = message.forward_from_chat.username
    else:
        # Пробуем распарсить введенный текст как ID
        try:
            channel_id = int(message.text)
        except ValueError:
            await message.answer("Неверный формат ID. Попробуйте еще раз или перешлите сообщение.")
            return

    try:
        # Проверяем, что бот администратор
        chat = await message.bot.get_chat(channel_id)
        title = chat.title
        username = chat.username
        
        await database.add_channel(channel_id, title, username)
        await state.clear()
        await message.answer(
            f"✅ Канал **{title}** успешно добавлен в базу!\n\nТеперь вы можете планировать в него посты.",
            reply_markup=keyboards.get_main_keyboard(),
            parse_mode="Markdown"
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка добавления канала. Убедитесь, что бот добавлен в администраторы канала.\n\nДетали: {e}")

# --- Создание отложенного поста ---
@router.callback_query(F.data == "create_post")
async def start_create_post(call: CallbackQuery, state: FSMContext):
    channels = await database.get_channels()
    if not channels:
        await call.answer("Сначала добавьте хотя бы один канал!", show_alert=True)
        return
        
    await call.message.edit_text(
        "Выберите канал для публикации:",
        reply_markup=keyboards.get_channels_keyboard(channels)
    )
    await state.set_state(PostStates.channel)

@router.callback_query(PostStates.channel, F.data.startswith("select_channel_"))
async def select_channel(call: CallbackQuery, state: FSMContext):
    channel_id = int(call.data.split("_")[2])
    await state.update_data(channel_id=channel_id)
    
    await call.message.edit_text(
        "Отправьте содержимое вашего поста. Это может быть обычный текст, фото с подписью или видео с подписью:",
        reply_markup=keyboards.get_cancel_keyboard()
    )
    await state.set_state(PostStates.content)

@router.message(PostStates.content)
async def process_content(message: Message, state: FSMContext):
    text = message.caption or message.text
    media_id = None
    media_type = None

    if message.photo:
        media_id = message.photo[-1].file_id
        media_type = "photo"
    elif message.video:
        media_id = message.video.file_id
        media_type = "video"

    await state.update_data(text=text, media_id=media_id, media_type=media_type)
    
    await message.answer(
        "Укажите дату и время отправки поста в формате:\n`ГГГГ-ММ-ДД ЧЧ:ММ`\n\nНапример: `2026-06-01 18:30`",
        reply_markup=keyboards.get_cancel_keyboard(),
        parse_mode="Markdown"
    )
    await state.set_state(PostStates.time)

@router.message(PostStates.time)
async def process_time(message: Message, state: FSMContext):
    time_str = message.text.strip()
    # Регулярка для проверки формата ГГГГ-ММ-ДД ЧЧ:ММ
    pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$"
    if not re.match(pattern, time_str):
        await message.answer("Неверный формат даты! Введите в формате: `ГГГГ-ММ-ДД ЧЧ:ММ`", parse_mode="Markdown")
        return
        
    try:
        run_date = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        if run_date < datetime.now():
            await message.answer("Нельзя запланировать пост в прошлое! Введите будущее время:")
            return
            
        data = await state.get_data()
        
        # Сохраняем в БД
        post_id = await database.create_post(
            text=data.get("text"),
            media_id=data.get("media_id"),
            media_type=data.get("media_type"),
            channel_id=data["channel_id"],
            scheduled_at=run_date
        )
        
        # Планируем в APScheduler
        schedule_post(
            bot=message.bot,
            post_id=post_id,
            channel_id=data["channel_id"],
            text=data.get("text"),
            media_id=data.get("media_id"),
            media_type=data.get("media_type"),
            run_date=run_date
        )
        
        await state.clear()
        await message.answer(
            f"✅ Пост успешно запланирован на **{time_str}**!",
            reply_markup=keyboards.get_main_keyboard(),
            parse_mode="Markdown"
        )
    except Exception as e:
        await message.answer(f"Произошла ошибка при обработке времени: {e}")

# --- Список запланированных ---
@router.callback_query(F.data == "list_scheduled")
async def show_scheduled(call: CallbackQuery):
    posts = await database.get_scheduled_posts()
    if not posts:
        await call.answer("У вас нет отложенных постов!", show_alert=True)
        return
        
    text = "📋 **Запланированные посты:**\n\n"
    for post in posts:
        media_mark = f" [{post['media_type']}]" if post['media_type'] else ""
        snippet = post['text'][:30] + "..." if post['text'] and len(post['text']) > 30 else (post['text'] or "")
        text += f"🔹 **Канал:** {post['channel_title']}\n📅 **Время:** {post['scheduled_at']}\n📝 **Пост:** {snippet}{media_mark}\n\n"
        
    await call.message.edit_text(text, reply_markup=keyboards.get_main_keyboard(), parse_mode="Markdown")

import os
from aiogram import Router, F, Bot, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import config
import database
import keyboards
from analytics import CRMAnalytics

router = Router()

class BroadcastStates(StatesGroup):
    waiting_for_message = State()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    # Save user to DB
    user_id = message.from_user.id
    username = message.from_user.username or "Anonymous"
    await database.add_user(user_id, username)
    
    welcome_text = (
        f"👋 **Привет, {message.from_user.first_name}!**\n\n"
        "Добро пожаловать в демонстрационного бота Nexus Labs CRM.\n"
        "Здесь ты можешь ознакомиться с услугами и симулировать покупку.\n\n"
        "⚙️ _Используйте кнопки ниже для выбора товара._"
    )
    
    await message.answer(welcome_text, reply_markup=keyboards.get_user_menu(), parse_mode="Markdown")
    
    # If this is the admin, send panel as well
    if user_id == config.ADMIN_ID:
        await message.answer("🔑 **Вы авторизованы как администратор.**\nИспользуйте `/admin` для доступа к CRM-панели.")

@router.message(Command("admin"))
async def cmd_admin(message: types.Message):
    if message.from_user.id != config.ADMIN_ID:
        await message.answer("❌ У вас нет доступа к этой команде.")
        return
        
    await message.answer("📊 **Админ-Панель управления Nexus CRM**", reply_markup=keyboards.get_admin_menu())

# --- User Callbacks (Simulated Purchases) ---

@router.callback_query(F.data.startswith("buy_"))
async def handle_purchase(callback: types.CallbackQuery):
    product = callback.data.split("_")[1]
    
    user_id = callback.from_user.id
    amount = 990.0 if product == "script" else 2490.0
    product_name = "Скрипт Автоматизации" if product == "script" else "Telegram-Бот под ключ"
    
    # Record sale in SQLite
    await database.record_sale(user_id, amount, product_name)
    
    await callback.answer("✅ Покупка симулирована!")
    await callback.message.answer(
        f"🎉 **Успешная оплата!**\n\n"
        f"Товар: `{product_name}`\n"
        f"Сумма: `{amount:.2f} руб.`\n"
        f"Транзакция успешно записана в базу данных CRM."
    )

# --- Admin Callbacks ---

@router.callback_query(F.data == "admin_users_count")
async def handle_users_count(callback: types.CallbackQuery):
    if callback.from_user.id != config.ADMIN_ID:
        await callback.answer("Доступ ограничен.", show_alert=True)
        return
        
    users = await database.get_all_users()
    await callback.answer()
    await callback.message.answer(f"👥 **Всего зарегистрированных пользователей:** `{len(users)}`")

@router.callback_query(F.data == "admin_stats")
async def handle_admin_stats(callback: types.CallbackQuery):
    if callback.from_user.id != config.ADMIN_ID:
        await callback.answer("Доступ ограничен.", show_alert=True)
        return
        
    await callback.answer("Генерация графиков...")
    
    image_path = await CRMAnalytics.generate_report_image()
    if image_path and os.path.exists(image_path):
        # Send photo
        photo = types.FSInputFile(image_path)
        await callback.message.answer_photo(
            photo=photo,
            caption="📈 **Аналитика за последние 7 дней**\n\n- Линия: регистрации пользователей\n- Столбцы: доход (руб.)"
        )
        # Cleanup file after sending
        os.remove(image_path)
    else:
        await callback.message.answer("⚠️ Не удалось сгенерировать аналитический отчет.")

@router.callback_query(F.data == "admin_broadcast")
async def handle_admin_broadcast(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id != config.ADMIN_ID:
        await callback.answer("Доступ ограничен.", show_alert=True)
        return
        
    await callback.answer()
    await state.set_state(BroadcastStates.waiting_for_message)
    await callback.message.answer(
        "✉️ **Режим массовой рассылки**\n\n"
        "Отправьте сообщение (текст, картинку или форматированный текст), "
        "которое нужно разослать всем зарегистрированным пользователям."
    )

@router.message(BroadcastStates.waiting_for_message)
async def process_broadcast(message: types.Message, state: FSMContext, bot: Bot):
    await state.clear()
    
    users = await database.get_all_users()
    if not users:
        await message.answer("❌ База данных пользователей пуста.")
        return
        
    status_msg = await message.answer(f"🚀 Начинаю рассылку для {len(users)} пользователей...")
    
    success = 0
    failed = 0
    
    for user_id in users:
        try:
            # Skip sending message to mock tokens or self to avoid API loops
            if user_id == message.from_user.id:
                # Still count as success to show demo works
                success += 1
                continue
                
            await bot.copy_message(
                chat_id=user_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
            success += 1
            await asyncio.sleep(0.05) # Rate limiting helper
        except Exception as e:
            failed += 1
            print(f"Failed sending to {user_id}: {e}")
            
    await status_msg.edit_text(
        f"🏁 **Рассылка завершена!**\n\n"
        f"✅ Успешно отправлено: `{success}`\n"
        f"❌ Ошибок отправки: `{failed}`"
    )

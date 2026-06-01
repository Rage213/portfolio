from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import database as db
import keyboards as kb
from config import ADMIN_ID

router = Router()

# State definitions for Admin Add Product workflow
class AddProductState(StatesGroup):
    name = State()
    description = State()
    price = State()

# --- COMMAND HANDLERS ---

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    welcome_text = (
        f"👋 **Привет, {message.from_user.first_name}!**\n\n"
        "🤖 Добро пожаловать в магазин цифровых услуг и готовых IT-решений!\n\n"
        "Здесь ты можешь заказать разработку Telegram-бота, парсера данных, "
        "готовые скрипты интеграции платежей или премиум-сайты.\n\n"
        "Выбирай интересующий раздел ниже 👇"
    )
    await message.answer(
        welcome_text, 
        reply_markup=kb.get_main_menu(message.from_user.id),
        parse_mode="Markdown"
    )

@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext):
    await state.clear()
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ У вас нет прав для доступа к этой команде.")
        return
        
    await message.answer(
        "🛡️ **Панель администратора магазина**\n\nЗдесь вы можете добавлять новые услуги и удалять существующие.",
        reply_markup=kb.get_admin_keyboard(),
        parse_mode="Markdown"
    )

# --- CALLBACK HANDLERS ---

@router.callback_query(F.data == "main_menu")
async def cb_main_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    welcome_text = (
        f"👋 **Привет, {callback.from_user.first_name}!**\n\n"
        "🤖 Добро пожаловать в магазин цифровых услуг и готовых IT-решений!\n\n"
        "Выбирай интересующий раздел ниже 👇"
    )
    await callback.message.edit_text(
        welcome_text,
        reply_markup=kb.get_main_menu(callback.from_user.id),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "catalog")
async def cb_catalog(callback: CallbackQuery):
    products = await db.get_all_products()
    if not products:
        await callback.message.edit_text(
            "🛍️ Каталог пуст.",
            reply_markup=kb.get_back_keyboard("main_menu")
        )
        return
        
    await callback.message.edit_text(
        "🛍️ **Каталог услуг и решений**\n\nВыберите интересующую позицию для просмотра подробностей:",
        reply_markup=kb.get_catalog_keyboard(products),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("prod_"))
async def cb_product_detail(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[1])
    product = await db.get_product_by_id(product_id)
    if not product:
        await callback.answer("❌ Товар не найден.", show_alert=True)
        return
        
    details_text = (
        f"🔥 **{product['name']}**\n\n"
        f"📝 {product['description']}\n\n"
        f"💰 Стоимость: **{product['price']} ₽**"
    )
    # Edit text block
    await callback.message.edit_text(
        details_text,
        reply_markup=kb.get_product_keyboard(product_id),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("buy_"))
async def cb_buy(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[1])
    product = await db.get_product_by_id(product_id)
    if not product:
        await callback.answer("❌ Товар не найден.", show_alert=True)
        return
        
    await db.add_to_cart(callback.from_user.id, product_id, 1)
    await callback.answer(f"➕ «{product['name']}» добавлен в корзину!", show_alert=False)

@router.callback_query(F.data == "cart")
async def cb_cart(callback: CallbackQuery):
    cart_items = await db.get_cart(callback.from_user.id)
    if not cart_items:
        await callback.message.edit_text(
            "🛒 **Ваша корзина пуста**\n\nПерейдите в каталог услуг, чтобы добавить товары.",
            reply_markup=kb.get_back_keyboard("main_menu"),
            parse_mode="Markdown"
        )
        return
        
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    
    cart_text = "🛒 **Ваша корзина заказа:**\n\n"
    for idx, item in enumerate(cart_items, 1):
        cart_text += f"{idx}. **{item['name']}**\n"
        cart_text += f"   └ {item['quantity']} шт. × {item['price']} ₽ = {item['quantity'] * item['price']} ₽\n\n"
        
    cart_text += f"💳 Итого к оплате: **{total} ₽**"
    
    await callback.message.edit_text(
        cart_text,
        reply_markup=kb.get_cart_keyboard(cart_items),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("cart_set_"))
async def cb_cart_set(callback: CallbackQuery):
    parts = callback.data.split("_")
    product_id = int(parts[2])
    qty = int(parts[3])
    
    await db.update_cart_item_qty(callback.from_user.id, product_id, qty)
    await cb_cart(callback) # Refresh cart view

@router.callback_query(F.data.startswith("cart_del_"))
async def cb_cart_del(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[2])
    await db.remove_from_cart(callback.from_user.id, product_id)
    await callback.answer("🗑️ Товар удален из корзины")
    await cb_cart(callback) # Refresh cart view

@router.callback_query(F.data == "cart_clear")
async def cb_cart_clear(callback: CallbackQuery):
    await db.clear_cart(callback.from_user.id)
    await callback.answer("🧹 Корзина очищена")
    await cb_cart(callback)

@router.callback_query(F.data == "checkout")
async def cb_checkout(callback: CallbackQuery):
    cart_items = await db.get_cart(callback.from_user.id)
    if not cart_items:
        await callback.answer("❌ Корзина пуста.", show_alert=True)
        return
        
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    
    # Store order in DB
    order_id = await db.create_order(callback.from_user.id, total)
    # Clear user's cart
    await db.clear_cart(callback.from_user.id)
    
    checkout_text = (
        f"🎉 **Заказ успешно сформирован!**\n\n"
        f"🆔 Номер заказа: **#{order_id}**\n"
        f"💰 Сумма к оплате: **{total} ₽**\n\n"
        f"💳 **Симуляция оплаты:**\n"
        f"Так как это демонстрационный бот, вы можете оплатить заказ тестовым переводом.\n"
        f"Для этого напишите разработчику в ЛС со скриншотом этого экрана:\n"
        f"👉 [Написать в Telegram](https://t.me/knrcharge)\n\n"
        f"Спасибо за доверие! Мы свяжемся с вами в течение часа."
    )
    await callback.message.edit_text(
        checkout_text,
        reply_markup=kb.get_back_keyboard("main_menu"),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

@router.callback_query(F.data == "info")
async def cb_info(callback: CallbackQuery):
    info_text = (
        "🤖 **О проекте Shop Bot**\n\n"
        "Этот бот — демонстрационный пример коммерческого проекта для фриланс-портфолио.\n\n"
        "💻 **Технологический стек:**\n"
        "• Язык: Python 3\n"
        "• Библиотека: aiogram 3.x (асинхронный Telegram Bot API)\n"
        "• База данных: aiosqlite (полностью неблокирующие дисковые запросы)\n"
        "• Архитектура: Событийно-ориентированная на базе роутеров и FSM (конечных автоматов)\n\n"
        "👨‍💻 **Контакты:**\n"
        "• Разработчик: @knrcharge\n"
        "• Исходный код доступен на GitHub!"
    )
    await callback.message.edit_text(
        info_text,
        reply_markup=kb.get_back_keyboard("main_menu"),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "noop")
async def cb_noop(callback: CallbackQuery):
    await callback.answer()

# --- ADMIN PANEL HANDLERS ---

@router.callback_query(F.data == "admin_panel")
async def cb_admin_panel(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ У вас нет прав.", show_alert=True)
        return
        
    await callback.message.edit_text(
        "🛡️ **Панель администратора магазина**\n\nВыберите действие:",
        reply_markup=kb.get_admin_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "admin_delete_list")
async def cb_admin_delete_list(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ У вас нет прав.", show_alert=True)
        return
        
    products = await db.get_all_products()
    if not products:
        await callback.message.edit_text(
            "🗑️ Нет товаров для удаления.",
            reply_markup=kb.get_back_keyboard("admin_panel")
        )
        return
        
    await callback.message.edit_text(
        "🗑️ **Выберите товар для удаления:**\n\nВнимание: удаление товара удалит его из всех каталогов.",
        reply_markup=kb.get_admin_delete_keyboard(products),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("admin_del_"))
async def cb_admin_del(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ У вас нет прав.", show_alert=True)
        return
        
    product_id = int(callback.data.split("_")[2])
    await db.delete_product(product_id)
    await callback.answer("🗑️ Товар успешно удален из базы данных")
    await cb_admin_delete_list(callback) # Refresh delete view

# --- FSM HANDLERS FOR ADDING PRODUCTS ---

@router.callback_query(F.data == "admin_add")
async def cb_admin_add(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ У вас нет прав.", show_alert=True)
        return
        
    await state.set_state(AddProductState.name)
    await callback.message.edit_text(
        "📝 **Добавление нового товара**\n\nШаг 1 из 3: Введите название товара (услуги):",
        reply_markup=kb.get_back_keyboard("admin_panel"),
        parse_mode="Markdown"
    )

@router.message(AddProductState.name)
async def process_add_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(AddProductState.description)
    await message.answer(
        "📝 **Шаг 2 из 3:**\n\nВведите подробное описание товара (услуги):",
        reply_markup=kb.get_back_keyboard("admin_panel"),
        parse_mode="Markdown"
    )

@router.message(AddProductState.description)
async def process_add_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text.strip())
    await state.set_state(AddProductState.price)
    await message.answer(
        "📝 **Шаг 3 из 3:**\n\nВведите стоимость товара в рублях (целое или дробное число):",
        reply_markup=kb.get_back_keyboard("admin_panel"),
        parse_mode="Markdown"
    )

@router.message(AddProductState.price)
async def process_add_price(message: Message, state: FSMContext):
    try:
        price = float(message.text.strip().replace(",", "."))
        if price < 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Пожалуйста, введите корректное положительное число для стоимости:")
        return
        
    user_data = await state.get_data()
    name = user_data['name']
    description = user_data['description']
    
    # Save product to database
    await db.add_product(name, description, price)
    await state.clear()
    
    success_text = (
        "✅ **Товар успешно добавлен в магазин!**\n\n"
        f"🛍️ Название: **{name}**\n"
        f"💰 Цена: **{price} ₽**"
    )
    await message.answer(
        success_text,
        reply_markup=kb.get_back_keyboard("admin_panel"),
        parse_mode="Markdown"
    )

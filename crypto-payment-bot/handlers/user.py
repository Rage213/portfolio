from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import database
import keyboards
from crypto_client import crypto_pay

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await database.add_user(message.from_user.id, message.from_user.username)
    await message.answer(
        f"Привет, {message.from_user.full_name}! Добро пожаловать в автоматический магазин цифровых товаров.\n\n"
        "Оплачивайте покупки криптовалютой с помощью удобной системы платежей.",
        reply_markup=keyboards.get_start_keyboard()
    )

@router.callback_query(F.data == "main_menu")
async def show_main_menu(call: CallbackQuery):
    await call.message.edit_text(
        "Добро пожаловать в автоматический магазин цифровых товаров.\n\n"
        "Оплачивайте покупки криптовалютой с помощью удобной системы платежей.",
        reply_markup=keyboards.get_start_keyboard()
    )

@router.callback_query(F.data == "catalog")
async def show_catalog(call: CallbackQuery):
    products = await database.get_products()
    if not products:
        await call.answer("Каталог пока пуст. Администратор скоро добавит товары!", show_alert=True)
        return
        
    await call.message.edit_text(
        "🛍️ Доступные товары:",
        reply_markup=keyboards.get_catalog_keyboard(products)
    )

@router.callback_query(F.data.startswith("buy_"))
async def process_buy(call: CallbackQuery):
    product_id = int(call.data.split("_")[1])
    product = await database.get_product(product_id)
    if not product:
        await call.answer("Товар не найден!", show_alert=True)
        return
        
    # Инициализация инвойса через Crypto Bot API
    invoice = await crypto_pay.create_invoice(
        amount=product["price_usd"],
        currency="USDT",
        description=str(product["id"])
    )
    
    if not invoice:
        await call.answer("Ошибка при создании счета. Попробуйте позже.", show_alert=True)
        return
        
    invoice_uuid = invoice["result"]["uuid"]
    pay_url = invoice["result"]["url"]
    
    # Записываем инвойс в базу данных
    await database.create_invoice(
        invoice_id=invoice_uuid,
        user_id=call.from_user.id,
        product_id=product["id"],
        amount=product["price_usd"]
    )
    
    await call.message.edit_text(
        f"🧾 **Счет на оплату товара:** {product['name']}\n"
        f"💵 **Сумма к оплате:** ${product['price_usd']} (USDT)\n\n"
        "Нажмите кнопку ниже для перехода к оплате. После оплаты нажмите кнопку проверки.",
        reply_markup=keyboards.get_payment_keyboard(pay_url, invoice_uuid),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("check_"))
async def check_payment(call: CallbackQuery):
    invoice_uuid = call.data.split("_")[1]
    invoice_db = await database.get_invoice(invoice_uuid)
    
    if not invoice_db:
        await call.answer("Счет не найден в базе данных!", show_alert=True)
        return
        
    if invoice_db["status"] == "paid":
        await call.answer("Этот счет уже оплачен и товар доставлен!", show_alert=True)
        return

    # Запрашиваем актуальный статус инвойса от API
    api_invoice = await crypto_pay.get_invoice(invoice_uuid)
    if api_invoice and api_invoice["result"]["status"] == "paid":
        # Успешная оплата
        await database.update_invoice_status(invoice_uuid, "paid")
        product = await database.get_product(invoice_db["product_id"])
        
        if product:
            await call.message.edit_text(
                f"🎉 **Оплата успешно подтверждена!**\n\n"
                f"📦 **Ваш оплаченный товар ({product['name']}):**\n\n"
                f"`{product['file_content']}`",
                parse_mode="Markdown"
            )
        else:
            await call.message.edit_text("Оплата получена, но товар был удален из базы. Свяжитесь с поддержкой.")
    else:
        await call.answer("Оплата пока не получена. Попробуйте проверить через минуту.", show_alert=True)

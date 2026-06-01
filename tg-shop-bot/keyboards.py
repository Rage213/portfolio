from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import ADMIN_ID

def get_main_menu(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🛍️ Каталог услуг", callback_data="catalog"),
        InlineKeyboardButton(text="🛒 Корзина", callback_data="cart")
    )
    builder.row(
        InlineKeyboardButton(text="💬 Написать мне", url="https://t.me/knrcharge"),
        InlineKeyboardButton(text="❓ FAQ / Инфо", callback_data="info")
    )
    
    # If the user is the configured admin, show Admin Panel button
    if user_id == ADMIN_ID:
        builder.row(InlineKeyboardButton(text="🛡️ Админ-панель", callback_data="admin_panel"))
        
    return builder.as_markup()

def get_catalog_keyboard(products: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for product in products:
        builder.row(InlineKeyboardButton(
            text=f"{product['name']} — {product['price']} ₽",
            callback_data=f"prod_{product['id']}"
        ))
    builder.row(InlineKeyboardButton(text="↩️ Главное меню", callback_data="main_menu"))
    return builder.as_markup()

def get_product_keyboard(product_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="➕ Добавить в корзину", callback_data=f"buy_{product_id}")
    )
    builder.row(
        InlineKeyboardButton(text="🛍️ К списку услуг", callback_data="catalog"),
        InlineKeyboardButton(text="🛒 В корзину", callback_data="cart")
    )
    return builder.as_markup()

def get_cart_keyboard(cart_items: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    # Render buttons to edit quantity or remove each item
    for item in cart_items:
        prod_id = item['product_id']
        qty = item['quantity']
        builder.row(
            InlineKeyboardButton(text=f"❌ {item['name']}", callback_data=f"cart_del_{prod_id}"),
            InlineKeyboardButton(text="➖", callback_data=f"cart_set_{prod_id}_{qty-1}"),
            InlineKeyboardButton(text=f"{qty} шт", callback_data="noop"),
            InlineKeyboardButton(text="➕", callback_data=f"cart_set_{prod_id}_{qty+1}")
        )
        
    if cart_items:
        builder.row(
            InlineKeyboardButton(text="🧹 Очистить", callback_data="cart_clear"),
            InlineKeyboardButton(text="💳 Оплатить", callback_data="checkout")
        )
        
    builder.row(InlineKeyboardButton(text="↩️ Назад в меню", callback_data="main_menu"))
    return builder.as_markup()

def get_admin_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="➕ Добавить товар", callback_data="admin_add"),
        InlineKeyboardButton(text="🗑️ Удалить товар", callback_data="admin_delete_list")
    )
    builder.row(InlineKeyboardButton(text="↩️ На главную", callback_data="main_menu"))
    return builder.as_markup()

def get_admin_delete_keyboard(products: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for product in products:
        builder.row(InlineKeyboardButton(
            text=f"❌ {product['name']}",
            callback_data=f"admin_del_{product['id']}"
        ))
    builder.row(InlineKeyboardButton(text="↩️ Назад в админку", callback_data="admin_panel"))
    return builder.as_markup()

def get_back_keyboard(callback_data: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="↩️ Назад", callback_data=callback_data))
    return builder.as_markup()

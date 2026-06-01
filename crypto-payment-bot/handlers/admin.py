from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import database
from config import ADMIN_IDS

router = Router()

class AddProductState(StatesGroup):
    name = State()
    description = State()
    price = State()
    content = State()

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("У вас нет прав для выполнения этой команды.")
        return
        
    await message.answer(
        "👑 **Панель Администратора**\n\n"
        "Команды:\n"
        "/add_product — Добавить новый товар в магазин\n"
        "/list_admin — Посмотреть все товары для удаления",
        parse_mode="Markdown"
    )

@router.message(Command("add_product"))
async def cmd_add_product(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
        
    await message.answer("Введите название нового товара:")
    await state.set_state(AddProductState.name)

@router.message(AddProductState.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите описание товара:")
    await state.set_state(AddProductState.description)

@router.message(AddProductState.description)
async def process_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите цену товара в долларах (например, 5.50):")
    await state.set_state(AddProductState.price)

@router.message(AddProductState.price)
async def process_price(message: Message, state: FSMContext):
    try:
        price = float(message.text)
        await state.update_data(price=price)
        await message.answer("Введите контент автовыдачи (код, ссылка, файл, текст):")
        await state.set_state(AddProductState.content)
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число:")

@router.message(AddProductState.content)
async def process_content(message: Message, state: FSMContext):
    data = await state.get_data()
    await database.create_product(
        name=data["name"],
        description=data["description"],
        price_usd=data["price"],
        file_content=message.text
    )
    await state.clear()
    await message.answer("✅ Товар успешно добавлен в каталог!")

@router.message(Command("list_admin"))
async def admin_list(message: Message):
    if not is_admin(message.from_user.id):
        return
        
    products = await database.get_products()
    if not products:
        await message.answer("Каталог пуст.")
        return
        
    text = "📦 **Список всех товаров:**\n\n"
    for product in products:
        text += f"ID: {product['id']} | **{product['name']}** — ${product['price_usd']}\nДля удаления: `/del_{product['id']}`\n\n"
        
    await message.answer(text, parse_mode="Markdown")

@router.message(F.text.regexp(r"^/del_\d+$"))
async def delete_product_cmd(message: Message):
    if not is_admin(message.from_user.id):
        return
        
    product_id = int(message.text.split("_")[1])
    product = await database.get_product(product_id)
    
    if not product:
        await message.answer("Товар не найден!")
        return
        
    await database.delete_product(product_id)
    await message.answer(f"✅ Товар '{product['name']}' успешно удален.")

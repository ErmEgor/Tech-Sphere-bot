# keyboards.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import CATALOG

# --- Главное меню ---
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛍️ Каталог")],
        [KeyboardButton(text="ℹ️ О нас")]
    ],
    resize_keyboard=True
)

# --- Клавиатуры каталога ---
def get_categories_kb():
    builder = InlineKeyboardBuilder()
    for category_id, category_data in CATALOG.items():
        builder.button(text=category_data['name'], callback_data=f"category:{category_id}")
    builder.adjust(1)
    return builder.as_markup()

def get_products_kb(category_id):
    builder = InlineKeyboardBuilder()
    products = CATALOG[category_id]['products']
    for product_id, product_data in products.items():
        builder.button(text=product_data['name'], callback_data=f"product:{category_id}:{product_id}")
    
    builder.button(text="◀️ Назад к категориям", callback_data="back_to_categories")
    builder.adjust(1)
    return builder.as_markup()

def get_product_details_kb(category_id, product_id):
    builder = InlineKeyboardBuilder()
    builder.button(text="🛒 Оформить заказ", callback_data=f"order:{product_id}")
    # <<< НОВАЯ КНОПКА >>>
    builder.button(text="📋 Характеристики", callback_data=f"specs:{category_id}:{product_id}")
    builder.button(text="◀️ Назад к товарам", callback_data=f"back_to_products:{category_id}")
    builder.adjust(2, 1) # Кнопки заказа и характеристик в один ряд
    return builder.as_markup()

# <<< НОВАЯ КЛАВИАТУРА >>>
def get_specs_kb(category_id, product_id):
    """Клавиатура для вида с характеристиками (только кнопка 'Назад к описанию')"""
    builder = InlineKeyboardBuilder()
    # Эта кнопка вернет пользователя к основному виду товара
    builder.button(text="◀️ Назад к описанию", callback_data=f"product:{category_id}:{product_id}")
    return builder.as_markup()

# --- Клавиатуры для формы заказа ---
payment_options_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Kaspi", callback_data="pay:kaspi")],
    [InlineKeyboardButton(text="Qiwi", callback_data="pay:qiwi")],
    [InlineKeyboardButton(text="Наличными при получении", callback_data="pay:cash")],
    [InlineKeyboardButton(text="Пропустить", callback_data="pay:skip")]
])

cancel_order_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="❌ Отменить заказ", callback_data="cancel_order")]
])
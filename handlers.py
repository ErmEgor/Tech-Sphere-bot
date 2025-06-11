# handlers.py
import re
import logging
from aiogram import Router, F, Bot, types
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.exceptions import TelegramBadRequest

import keyboards as kb
from config import ADMIN_ID, CATALOG

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
logger = logging.getLogger(__name__)

# Создаем роутер
router = Router()

# --- Состояния FSM для заказа ---
class OrderState(StatesGroup):
    getting_name = State()
    getting_phone = State()
    getting_city = State()
    getting_payment = State()
    getting_comment = State()

# --- Обработчики команд и главного меню ---
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Добро пожаловать в Tech Sphere! 🪐\n\n"
        "Здесь вы найдете лучшие гаджеты по отличным ценам. "
        "Нажмите на кнопку ниже, чтобы посмотреть наш ассортимент.",
        reply_markup=kb.main_kb
    )

@router.message(F.text == "ℹ️ О нас")
async def about_us(message: Message):
    about_text = (
        "<b>Tech Sphere 🪐 — ваш гид в мире современных гаджетов!</b>\n\n"
        "Мы не просто продаем технику. Мы помогаем вам найти идеальные устройства, которые сделают вашу жизнь ярче, удобнее и продуктивнее.\n\n"
        "<b>Наши принципы:</b>\n"
        "✅ <b>Только оригинальная продукция:</b> Мы работаем с проверенными поставщиками и гарантируем подлинность каждого товара.\n"
        "🚀 <b>Быстрая доставка:</b> Отправляем заказы по всему Казахстану в кратчайшие сроки.\n"
        "💬 <b>Экспертная поддержка:</b> Наша команда всегда готова помочь с выбором и ответить на любые вопросы.\n\n"
        "<i>Свяжитесь с нами, и мы подберем гаджет вашей мечты!</i>"
    )
    await message.answer(about_text, reply_markup=kb.main_kb)

@router.message(Command("cancel"))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Действие отменено.", reply_markup=kb.main_kb)

@router.callback_query(F.data == "cancel_order")
async def cq_cancel_order(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete() # Удаляем сообщение с отменой
    await callback.message.answer("Заказ отменен. Вы вернулись в главное меню.", reply_markup=kb.main_kb)
    await callback.answer()

# --- Обработчики каталога ---
@router.message(F.text == "🛍️ Каталог")
async def show_catalog(message: Message):
    await message.answer("Выберите категорию:", reply_markup=kb.get_categories_kb())

@router.callback_query(F.data.startswith("category:"))
async def show_products(callback: CallbackQuery):
    try:
        prefix, category_id = callback.data.split(":", maxsplit=1)
        if category_id not in CATALOG:
            await callback.answer("Категория не найдена!", show_alert=True)
            return
        
        await callback.message.edit_text(
            f"Товары в категории «{CATALOG[category_id]['name']}»:",
            reply_markup=kb.get_products_kb(category_id)
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка в show_products: {e}")
        await callback.answer("Произошла ошибка!", show_alert=True)

@router.callback_query(F.data == "back_to_categories")
async def back_to_categories(callback: CallbackQuery):
    await callback.message.edit_text("Выберите категорию:", reply_markup=kb.get_categories_kb())
    await callback.answer()

# <<< ИСПРАВЛЕННЫЙ ОБРАБОТЧИК ДЛЯ ПОКАЗА ТОВАРА И ВОЗВРАТА К НЕМУ >>>
@router.callback_query(F.data.startswith("product:"))
async def show_product_details(callback: CallbackQuery):
    try:
        prefix, category_id, product_id = callback.data.split(":", maxsplit=2)
        
        if category_id not in CATALOG or product_id not in CATALOG[category_id]['products']:
            await callback.answer("Товар не найден!", show_alert=True)
            return

        product = CATALOG[category_id]['products'][product_id]
        price_formatted = f"{product['price']:,}".replace(',', ' ')
        caption = (
            f"<b>{product['name']}</b>\n\n"
            f"{product['desc']}\n\n"
            f"<b>Цена:</b> {price_formatted} ₸"
        )
        
        # Если у сообщения есть фото, мы просто меняем его подпись (caption).
        # Если фото нет (это текстовое сообщение), мы его удаляем и отправляем фото.
        if callback.message.photo:
            await callback.message.edit_caption(
                caption=caption,
                reply_markup=kb.get_product_details_kb(category_id, product_id)
            )
        else:
            await callback.message.delete()
            await callback.message.answer_photo(
                photo=product['photo'],
                caption=caption,
                reply_markup=kb.get_product_details_kb(category_id, product_id)
            )
        await callback.answer()

    except Exception as e:
        logger.error(f"Общая ошибка в show_product_details: {e}")
        await callback.answer("Произошла ошибка при отображении товара!", show_alert=True)

# <<< НОВЫЙ ОБРАБОТЧИК ДЛЯ ХАРАКТЕРИСТИК >>>
@router.callback_query(F.data.startswith("specs:"))
async def show_product_specs(callback: CallbackQuery):
    try:
        prefix, category_id, product_id = callback.data.split(":", maxsplit=2)
        
        if category_id not in CATALOG or product_id not in CATALOG[category_id]['products']:
            await callback.answer("Товар не найден!", show_alert=True)
            return

        product = CATALOG[category_id]['products'][product_id]
        
        # Создаем текст с характеристиками
        caption = (
            f"<b>{product['name']} - Характеристики</b>\n\n"
            f"{product['specs']}"
        )
        
        # Редактируем подпись у существующего фото
        await callback.message.edit_caption(
            caption=caption,
            reply_markup=kb.get_specs_kb(category_id, product_id)
        )
        await callback.answer()

    except Exception as e:
        logger.error(f"Ошибка в show_product_specs: {e}")
        await callback.answer("Произошла ошибка!", show_alert=True)

@router.callback_query(F.data.startswith("back_to_products:"))
async def back_to_products(callback: CallbackQuery):
    try:
        prefix, category_id = callback.data.split(":", maxsplit=1)
        
        if category_id not in CATALOG:
            await callback.answer("Категория не найдена!", show_alert=True)
            return
        
        # Удаляем сообщение с фото и отправляем новое со списком товаров
        await callback.message.delete()
        await callback.message.answer(
            text=f"Товары в категории «{CATALOG[category_id]['name']}»:",
            reply_markup=kb.get_products_kb(category_id)
        )
        await callback.answer()

    except Exception as e:
        logger.error(f"Ошибка в back_to_products: {e}")
        await callback.answer("Произошла ошибка при возврате!", show_alert=True)

#@router.message(F.photo)
#async def log_photo(message: types.Message):
    #file_id = message.photo[-1].file_id
    #logger.info(f"File ID: {file_id}")
    #await message.answer(f"File ID: {file_id}")

# --- FSM для оформления заказа ---
@router.callback_query(F.data.startswith("order:"))
async def start_order(callback: CallbackQuery, state: FSMContext):
    try:
        prefix, product_id = callback.data.split(":", maxsplit=1)
        
        product_to_order = None
        for category in CATALOG.values():
            if product_id in category['products']:
                product_to_order = category['products'][product_id]
                break

        if not product_to_order:
            await callback.answer("Товар не найден!", show_alert=True)
            return
            
        await state.update_data(product_name=product_to_order['name'])
        await state.set_state(OrderState.getting_name)

        await callback.message.delete()
        await callback.message.answer(
            "Для оформления заказа, пожалуйста, введите ваше имя:",
            reply_markup=kb.cancel_order_kb
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка в start_order: {e}")
        await callback.answer("Произошла ошибка!", show_alert=True)

@router.message(StateFilter(OrderState.getting_name))
async def get_name(message: Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    await state.set_state(OrderState.getting_phone)
    await message.answer(
        "Отлично! Теперь введите ваш номер телефона (например, +77071234567):",
        reply_markup=kb.cancel_order_kb
    )

@router.message(StateFilter(OrderState.getting_phone))
async def get_phone(message: Message, state: FSMContext):
    if not re.match(r'^\+?\d{10,15}$', message.text):
        await message.answer(
            "Неверный формат номера. Пожалуйста, введите корректный номер телефона.",
            reply_markup=kb.cancel_order_kb
        )
        return
    
    await state.update_data(phone=message.text)
    await state.set_state(OrderState.getting_city)
    await message.answer(
        "Спасибо. Укажите ваш город:",
        reply_markup=kb.cancel_order_kb
    )

@router.message(StateFilter(OrderState.getting_city))
async def get_city(message: Message, state: FSMContext):
    city_name = message.text.strip()
    
    if len(re.findall(r'[а-яА-ЯёЁ]', city_name)) < 3 or not re.fullmatch(r'[а-яА-ЯёЁ\s-]{3,50}', city_name):
        await message.answer(
            "Некорректное название города. Пожалуйста, введите город кириллицей (мин. 3 буквы). Например: Алматы, Нур-Султан, Караганда.",
            reply_markup=kb.cancel_order_kb
        )
        return
    
    await state.update_data(city=city_name.capitalize())
    await state.set_state(OrderState.getting_payment)
    await message.answer(
        "Как вам будет удобно оплатить?",
        reply_markup=kb.payment_options_kb
    )

@router.callback_query(StateFilter(OrderState.getting_payment), F.data.startswith("pay:"))
async def get_payment(callback: CallbackQuery, state: FSMContext):
    payment_method_map = {
        "kaspi": "Kaspi",
        "qiwi": "Qiwi",
        "cash": "Наличными при получении",
        "skip": "Уточнить у клиента"
    }
    prefix, payment_key = callback.data.split(':', maxsplit=1)
    payment_method = payment_method_map.get(payment_key, "Не указан")
        
    await state.update_data(payment=payment_method)
    await state.set_state(OrderState.getting_comment)
    await callback.message.edit_text(
        "Оставьте комментарий к заказу (например, количество, адрес, пожелания) или напишите 'нет':",
        reply_markup=kb.cancel_order_kb
    )
    await callback.answer()

@router.message(StateFilter(OrderState.getting_comment))
async def get_comment_and_finish(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(comment=message.text)
    
    data = await state.get_data()
    
    admin_message = (
        f"📦 <b>Новый заказ!</b>\n\n"
        f"👤 <b>Имя:</b> {data.get('user_name')}\n"
        f"📱 <b>Телефон:</b> <code>{data.get('phone')}</code>\n"
        f"🏠 <b>Город:</b> {data.get('city')}\n"
        f"🛒 <b>Товар:</b> {data.get('product_name')}\n"
        f"💳 <b>Оплата:</b> {data.get('payment')}\n"
        f"💬 <b>Комментарий:</b> {data.get('comment')}\n\n"
        f"👤 <b>Telegram:</b> @{message.from_user.username} (ID: <code>{message.from_user.id}</code>)"
    )
    
    try:
        await bot.send_message(ADMIN_ID, admin_message)
        await message.answer(
            "🎉 <b>Ваш заказ успешно оформлен!</b>\n\n"
            "Наш менеджер скоро свяжется с вами для подтверждения деталей. Спасибо за покупку!",
            reply_markup=kb.main_kb
        )
    except Exception as e:
        await message.answer(
            "😕 Произошла ошибка при отправке заказа. Пожалуйста, попробуйте снова позже.",
            reply_markup=kb.main_kb
        )
        logger.error(f"Ошибка при отправке заказа админу: {e}")

    await state.clear()
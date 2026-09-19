import aiogram
import asyncio
import sqlite3
import os
import aiohttp
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart

from dotenv import load_dotenv
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

load_dotenv()
my_bot_token = os.getenv("BOT_TOKEN")
admin_id = os.getenv("ADMIN_ID")

bot = Bot(token=my_bot_token, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

class OrderState(StatesGroup):
    name = State()
    description = State()
    budget = State()


text = """👋 Привет, <b>{name}</b>! 

Я <b>Руслан</b> — Python-разработчик. 
Помогаю бизнесу автоматизировать рутину с помощью 🤖 Telegram-ботов и 🕷 сбора данных.

👇 <i>Выберите нужный раздел ниже:</i>"""

inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Обо мне", callback_data="my_profile")],
        [InlineKeyboardButton(text="Мои проекты", callback_data="my_projects")],
        [InlineKeyboardButton(text="Заказать бота/парсер", callback_data="make_order")]
    ]
)

inline_keyboard_projects = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Магазин Volley", callback_data="volley_shop")],
        [InlineKeyboardButton(text="Парсер Цитат", callback_data="quotes_parser")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_menu")]
    ]
)

inline_keyboard_return = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back_to_menu")]
    ]
)
@dp.message(CommandStart())
async def start_message(message: Message):
    await message.answer(
f"""👋 Привет, <b>{message.from_user.first_name}</b>! 

    Я <b>Руслан</b> — Python-разработчик. 
    
Помогаю бизнесу автоматизировать рутину с помощью 🤖 Telegram-ботов и 🕷 сбора данных.

👇 <i>Выберите нужный раздел ниже:</i>""", reply_markup=inline_keyboard)

@dp.callback_query(F.data=="my_profile")
async def my_profile(callback: CallbackQuery):
    await callback.message.edit_text("""Меня зовут Руслан и я Python-разработчик.
                        Мой основной стек:
                                                  
<b>🤖 Telegram боты</b>:
🔹 Проектирование сложных сценариев (FSM) и анти-краш систем
🔹 Интеграция баз данных (SQLite) для учета клиентов и заказов.
🔹 Подключение реальных касс (Telegram Payments, Stripe, ЮKassa)
🔹 Разработка удобных и динамичных инлайн-интерфейсов

<b>🕷 Веб-парсинг</b>:
🔹 Сбор данных с многостраничных сайтов (пагинация)
🔹 Упаковка собранной информации в удобные CSV/Excel отчеты для аналитики

👇 <i>Выберите раздел ниже, чтобы посмотреть мои работы или сделать заказ</i>""", reply_markup=inline_keyboard_return)


@dp.callback_query(F.data=="my_projects")
async def my_projects(callback: CallbackQuery):
    await callback.message.edit_text("Вот мои текущие проекты:", reply_markup=inline_keyboard_projects)

@dp.callback_query(F.data=="volley_shop")
async def volley_shop(callback: CallbackQuery):
    await callback.message.edit_text(
        """ <b>👟 VolleyShop</b> — Магазин спортивной обуви

Что реализовано:
🔹 Оформление заказа через FSM (машину состояний)
🔹 Защита от спама и неверного ввода (анти-краш)
🔹 Сохранение данных клиентов в базу SQLite
🔹 Подключение оплаты картой внутри бота

🔗 Исходный код: https://github.com/TheQwency/volleyshop-telegram-bot
    
    """, reply_markup=inline_keyboard_return)


@dp.callback_query(F.data == "quotes_parser")
async def quotes_parser(callback: CallbackQuery):
    await callback.message.edit_text(
        """ <b>📈 Крипто-трекер</b> 

Что реализовано:
🔹 Интеграция со сторонними REST API сервисами
🔹 Асинхронные HTTP-запросы для моментального отклика
🔹 Парсинг и обработка JSON-ответов от сервера
🔹 Удобный пользовательский интерфейс для запроса данных

🔗 Исходный код: https://github.com/TheQwency/bitcoin-tracker-bot

    """, reply_markup=inline_keyboard_return)

@dp.callback_query(F.data == "make_order")
async def make_order(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        """Отлично! Чтобы совершить заказ мне нужны некоторые подробности:
        
<b>Шаг 1</b>: Как я могу к вам обращаться?""")

    await state.set_state(OrderState.name)


@dp.message(OrderState.name, F.text)
async def make_order_state(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer(
        """Приятно познакомиться! 
        
<b>Шаг 2:</b> Опишите вкратце, какого бота или парсер вам нужно разработать?""")

    await state.set_state(OrderState.description)

@dp.message(OrderState.name)
async def name_state_defense(message: Message, ):
    await message.answer("Пожалуйста ответьте обычным текстом")

@dp.message(OrderState.description, F.text)
async def description_state(message: Message, state: FSMContext):
    await state.update_data(description=message.text)

    await message.answer("""Описание принял. 
    
    <b>Шаг 3:</b> Какой у вас бюджет?
    """)

    await state.set_state(OrderState.budget)

@dp.message(OrderState.description)
async def description_state_defense(message: Message, ):
    await message.answer("Пожалуйста ответьте обычным текстом")



@dp.message(OrderState.budget, F.text)
async def budget_state(message: Message, state: FSMContext):
    await state.update_data(budget=message.text)

    await message.answer("🔥 Отлично! Вся нужная информация взята. И заявка успешна подана")

    user_nickname = message.from_user.username

    data = await state.get_data()

    await bot.send_message(chat_id=admin_id, text=
    f"""🔥 <b>Новый Заказ!</b>
Имя: {data['name']};
Описание: {data['description']};
Бюджет: {data['budget']};   

<b>Заказчик</b>: <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>.
    
    """)

    await state.clear()


@dp.callback_query(F.data=="back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        f"""👋 Привет, <b>{callback.from_user.first_name}</b>! 

    Я <b>Руслан</b> — Python-разработчик. 
    
Помогаю бизнесу автоматизировать рутину с помощью 🤖 Telegram-ботов и 🕷 сбора данных.

👇 <i>Выберите нужный раздел ниже:</i>""", reply_markup=inline_keyboard)



async def main():
    await dp.start_polling(bot)

    pass




if __name__ == "__main__":
    asyncio.run(main())
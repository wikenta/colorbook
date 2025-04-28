import asyncio
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, LoginUrl
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply, WebAppInfo, LabeledPrice
from db_request.publisher import get_publishers
from db_request.volume import get_books_by_publisher

router = Router()

# Хендлер для команды /books
@router.message(F.text == "/books")
async def send_books(message: Message):
    response = "Список книг:\n\n"

    publishers = await get_publishers()
    for publisher in publishers:
        books = await get_books_by_publisher(publisher['id'])
        if books:
            response += f"Издатель: {publisher['name_ru']}\n"
            for book in books:
                response += f"{book['full_name_ru']}"
                if book['release_year']:
                    response += f" ({book['release_year']})"
                response += "\n"
            response += "\n"

    if not response:
        response = "Книги не найдены."

    await message.reply(response, parse_mode="Markdown")

# Хендлер на стартовую команду
@router.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.reply("Привет! Бот еще разрабатывается. Загляни позже, скоро появятся новые функции")

buttons = [
    [InlineKeyboardButton(text="Кнопка 1", callback_data="button1")],
    [InlineKeyboardButton(text="Кнопка 2", callback_data="button2")],
    [InlineKeyboardButton(text="Кнопка 3", callback_data="button3")],
    [InlineKeyboardButton(text="URL-кнопка", url="https://example.com")],
    [InlineKeyboardButton(text="Логин", login_url=LoginUrl(url="https://example.com/login"))],
    [InlineKeyboardButton(text="Запросить контакт", callback_data="request_contact")],
    [InlineKeyboardButton(text="Запросить локацию", callback_data="request_location")]
]

# Тестируем кнопки
@router.message(F.text == "/test_buttons")
async def test_buttons(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.reply("Выберите кнопку:", reply_markup=keyboard)

@router.callback_query(F.data == "button1")
async def handle_button1(callback_query: CallbackQuery):
    await callback_query.answer("Вы нажали кнопку 1!", show_alert=True)
    # Вместо удаления клавиатуры - редактируем сообщение
    await callback_query.message.edit_text(
        "Вы выбрали Кнопку 1!\nХотите сделать что-то еще?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Вернуться", callback_data="back_to_menu")]
        ])
    )

@router.callback_query(F.data == "button2")
async def handle_button2(callback_query: CallbackQuery):
    await callback_query.answer("Вы нажали кнопку 2!", show_alert=False)  # Всплывающее уведомление

@router.callback_query(F.data == "button3")
async def handle_button2(callback_query: CallbackQuery):
    await callback_query.message.reply("Вы выбрали Кнопку 3! Что дальше?")

@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback_query: CallbackQuery):
    # Возвращаем исходное меню
    await callback_query.message.edit_text(
        "Выберите кнопку:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )

@router.message(F.text == "/test_reply_buttons")
async def test_reply_buttons(message: Message):
    markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Отправить контакт", request_contact=True)],
        [KeyboardButton(text="Отправить локацию", request_location=True)],
        [KeyboardButton(text="Обычная кнопка")]
    ], resize_keyboard=True)
    await message.answer("Выберите действие:", reply_markup=markup)

@router.message(F.text == "Отправить контакт")
async def handle_contact(message: Message):
    await message.answer("Контакт получен!")

@router.message(F.text == "Отправить локацию")
async def handle_location(message: Message):
    await message.answer("Локация получена!")

@router.message(F.text == "/remove_buttons")
async def remove_buttons(message: Message):
    await message.answer(
        "Клавиатура скрыта",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(F.text == "/test_force_reply")
async def test_force_reply(message: Message):
    await message.answer(
        "Напишите что-нибудь в ответ:",
        reply_markup=ForceReply(input_field_placeholder="Ваш ответ...")
    )

@router.message(F.text == "/test_callback_args")
async def test_callback_args(message: Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Действие 1", callback_data="action:1")],
        [InlineKeyboardButton(text="Действие 2", callback_data="action:2")]
    ])
    await message.answer("Выберите действие:", reply_markup=markup)

@router.callback_query(F.data.startswith("action:"))
async def handle_action(callback: CallbackQuery):
    action_id = callback.data.split(":")[1]
    await callback.answer(f"Выбрано действие {action_id}", show_alert=True)

@router.message(F.text == "/test_emoji_buttons")
async def test_emoji_buttons(message: Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel")],
        [InlineKeyboardButton(text="⭐ Избранное", callback_data="favorite")]
    ])
    await message.answer("Выберите:", reply_markup=markup)

@router.message(F.text == "/test_webapp")
async def test_webapp(message: Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Открыть веб-приложение",
            web_app=WebAppInfo(url="https://example.com")
        )]
    ])
    await message.answer("Тест WebApp:", reply_markup=markup)

@router.message(F.text == "/test_payment")
async def test_payment(message: Message):
    await message.answer_invoice(
        title="Тестовая оплата",
        description="Платеж для тестирования",
        payload="test_payload",
        provider_token="YOUR_PAYMENT_TOKEN",
        currency="RUB",
        prices=[LabeledPrice(label="Тест", amount=10000)],  # 100 RUB
        start_parameter="test-payment"
    )

@router.message(F.text == "/test_timer_button")
async def test_timer_button(message: Message):
    msg = await message.answer("Таймер: 10 сек", reply_markup=InlineKeyboardMarkup(inline_keyboard=
        [InlineKeyboardButton(text="Отмена", callback_data="cancel_timer")]
    ))

    for i in range(9, 0, -1):
        await asyncio.sleep(1)
        await msg.edit_text(f"Таймер: {i} сек")

    await msg.edit_text("Время вышло!", reply_markup=None)
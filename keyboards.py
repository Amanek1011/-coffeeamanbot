
from aiogram.types import (ReplyKeyboardMarkup,KeyboardButton,
                           InlineKeyboardMarkup ,InlineKeyboardButton)


coffee_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🍫 Какао", callback_data="kakao")],
    [InlineKeyboardButton(text="☕ Латте", callback_data="latte")],
    [InlineKeyboardButton(text="🥛 Капучино", callback_data="cappuccino")]
])

size_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Маленький"), KeyboardButton(text="Средний"), KeyboardButton(text="Большой")]
], resize_keyboard=True, one_time_keyboard=True)

confirm_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Подтвердить заказ", callback_data="confirm")],
    [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
])

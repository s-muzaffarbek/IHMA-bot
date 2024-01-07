from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
languages = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 O`zbekcha", callback_data="lang:uz"),
            InlineKeyboardButton(text="🇷🇺 Русский",callback_data="lang:ru"),
        ],
    ]
)

contact = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📞 Raqamni yuborish", request_contact=True),
        ],
    ],
    resize_keyboard=True
)

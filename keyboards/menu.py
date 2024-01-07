from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Agentlikka murojaatlar")
        ],
        [
            KeyboardButton(text="Nogironligi bo'lgan shaxslar"),
        ],
        [
            KeyboardButton(text="Yoshga doir nafaqalar"),
        ]
    ],
    resize_keyboard=True
)
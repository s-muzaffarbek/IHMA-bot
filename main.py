import re
from aiogram import executor

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart, Command
from aiogram.types import InlineKeyboardButton, ContentTypes

from data.config import ADMINS
from keyboards.language import languages, contact
from keyboards.menu import menu
from loader import dp
from aiogram import types
from states.userData import DataForm


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message):
    await message.answer(f"Tilni tanlang", reply_markup=languages)


@dp.callback_query_handler(lambda c: c.data.startswith('lang:'), state="*")
async def set_language(call: types.CallbackQuery):
    lang = call.data.split(':')[-1]
    if lang == "uz":
        await call.message.edit_text("🇺🇿 O'zbek tili tanlandi")
        await call.message.answer("Tanlang", reply_markup=menu)
        await call.answer(cache_time=60)


@dp.message_handler(
    lambda message: message.text in ["Agentlikka murojaatlar", "Nogironligi bo'lgan shaxslar", "Yoshga doir nafaqalar"],
    state="*")
async def select_vacancy(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['yonalish'] = message.text
        await message.answer("Ism va familiyangizni kiriting:", reply_markup=types.ReplyKeyboardRemove())
    await DataForm.name.set()


@dp.message_handler(state=DataForm.name)
async def enter_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer("Telefon raqamingizni kiriting:", reply_markup=contact)
    await DataForm.next()


@dp.message_handler(lambda message: not message.text.startswith('+'), state=DataForm.phone)
async def enter_phone_invalid(message: types.Message):
    await message.answer(
        "Telefon raqamingizni noto'g'ri formatda kiritdingiz. Iltimos, to'g'ri formatda kiriting (masalan, +998901234567).")


@dp.message_handler(state=DataForm.phone, content_types=ContentTypes.CONTACT)
@dp.message_handler(lambda message: not re.match(r'^\d+$', message.text), state=DataForm.phone)
async def enter_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.contact != None:
            contact = message.contact
            phone = contact.phone_number
        else:
            phone = message.text
        data['phone'] = phone
        data['user_id'] = message.from_user.id
    await message.answer("Murojaatingizni kiriting: ", reply_markup=types.ReplyKeyboardRemove())
    await DataForm.next()

@dp.message_handler(state=DataForm.description)
async def enter_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text

    await message.answer("Murojaatingiz qabul qilindi!\nRaxmat!")

    await dp.bot.send_message(chat_id=ADMINS[0],
                              text=f"<b>{data['yonalish']}</b>\n\n"
                                   f"Ismi, Familiyasi: <b>{data['name']}</b>\n"
                                   f"Telefon raqami: <b>{data['phone']}</b>\n"
                                   f"Murojaati : {data['description']}")

    # forward = await dp.bot.forward_message(chat_id=ADMINS[1],
    #                              from_chat_id=message.chat.id,
    #                              message_id=message.message_id)
    #
    # admin_reply_message_id = forward.message_id
    # await state.update_data(admin_reply_message_id=admin_reply_message_id)

    await state.finish()

# Handling admin replies
# @dp.message_handler(lambda message: message.reply_to_message and message.reply_to_message.forward_from_chat and message.from_user.id in ADMINS)
# async def forward_admin_reply_to_user(message: types.Message):
#     admin_reply_message_id = message.reply_to_message.message_id
#
#     if message.reply_to_message.forward_from_chat.id == ADMINS[1]:
#         user_id = message.reply_to_message.forward_sender_id  # Extracting the original user ID from the forwarded message
#
#         # Forwarding admin's reply to the user
#         await dp.bot.send_message(user_id, message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


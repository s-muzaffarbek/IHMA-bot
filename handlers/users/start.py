# from typing import re
#
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.builtin import CommandStart, Command
# from aiogram.types import InlineKeyboardButton, ContentTypes
#
# from data.config import ADMINS
# from keyboards.language import languages, contact
# from keyboards.menu import menu
# from loader import dp, bot
# from aiogram import types
#
# from states.userData import DataForm
#
#
# @dp.message_handler(CommandStart(), state="*")
# async def bot_start(message: types.Message):
#     await message.answer(f"Tilni tanlang", reply_markup=languages)
#
#
# @dp.message_handler(lambda message: message.text in ["Agentlikka murojaatlar", "Nogironligi bo'lgan shaxslar", "Yoshga doir nafaqalar"],  state="*")
# async def select_vacancy(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['yonalish'] = message.text
#         await message.answer("Ism va familiyangizni kiriting:")
#     await DataForm.name.set()
#
# @dp.message_handler(state=DataForm.name)
# async def enter_name(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['name'] = message.text
#     await message.answer("Telefon raqamingizni kiriting:", reply_markup=contact)
#     await DataForm.next()
#
#
# @dp.message_handler(lambda message: not message.text.startswith('+'), state=DataForm.phone)
# async def enter_phone_invalid(message: types.Message):
#     await message.answer(
#         "Telefon raqamingizni noto'g'ri formatda kiritdingiz. Iltimos, to'g'ri formatda kiriting (masalan, +998901234567).")
#
#
# @dp.message_handler(state=DataForm.phone, content_types=ContentTypes.CONTACT)
# @dp.message_handler(lambda message: not re.match(r'^\d+$', message.text), state=DataForm.phone)
# async def enter_phone(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         if message.contact != None:
#             contact = message.contact
#             phone = contact.phone_number
#         else:
#             phone = message.text
#         data['phone'] = phone
#         data['user_id'] = message.from_user.id
#     await message.answer("Murojaatingizni kiriting: ", reply_markup=types.ReplyKeyboardRemove())
#     await DataForm.next()
#
# @dp.message_handler(state=DataForm.description)
# async def enter_description(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['description'] = message.text
#
#     await message.answer("Murojaatingiz qabul qilindi!\n Raxmat!", reply_markup=menu)
#
#     await dp.bot.forward_message(chat_id=ADMINS[1],
#                                  message_id=data['user_id'],
#                                     text=f"<b>{data['name']}</b>\n\n"
#                                     f"Ismi, Familiyasi: <b>{data['name']}</b>\n"
#                                     f"Telefon raqami: <b>{data['phone']}</b>\n"
#                                     f"Qo'shimcha : {data['description']}")
#
#     await state.finish()
#

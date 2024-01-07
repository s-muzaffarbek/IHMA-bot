from aiogram.dispatcher.filters.state import StatesGroup, State

class DataForm(StatesGroup):
    user_id = State()
    name = State()
    phone = State()
    description = State()
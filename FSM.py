from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMUser(StatesGroup):
    name_of_exs = State()
    data = State()

class FSMAutomatic(StatesGroup):
    muscular_group = State()

class FSMRewriting(StatesGroup):
    date_and_exercise_to_query = State()
    new_data_to_update = State()

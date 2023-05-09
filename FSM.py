from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMUser(StatesGroup):
    name_of_exs = State()
    data = State()


class FSMAutomatic(StatesGroup):
    muscular_group = State()


class FSMRewriting(StatesGroup):
    date_to_rewrite = State()
    exercise_to_rewrite = State()
    ok_state = State()
    new_data_to_update = State()


class FSHHistory(StatesGroup):
    exercises_to_query = State()


class BuySub(StatesGroup):
    buying_state = State()
    photo = State()

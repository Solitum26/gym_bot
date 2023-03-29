import pandas as pd
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from commands_text import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboard import dictionary_of_menu
from datetime import date
from FSM import FSMUser, FSMAutomatic, FSMContext
from connect_to_SQL import *
from psycopg2.sql import Literal
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

storage = MemoryStorage()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=storage)

# начальный экран
@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.answer(text=start_text, reply_markup=dictionary_of_menu['main_menu'])

# Хендлер окна помощи
@dp.message_handler(commands=['help'])
async def start_message(message: types.Message):
    await message.answer(text=help_text)

# Хендлер новой тренировки
@dp.message_handler(commands=['new_train'])
async def type_of_train(message: types.Message, state: FSMContext):
    await FSMAutomatic.muscular_group.set()
    await message.answer(text=add_new_train_text, reply_markup=dictionary_of_menu['muscular_menu'])

# Хендлер просмотра БД
@dp.message_handler(commands=['check_history'])
async def query(message: types.Message):
    try:
        exercise_to_query = message.text.split()[1]
        df = pd.read_sql_query(f"""
        SELECT date, train_params
        FROM exercises_data
        WHERE exercise = '{exercise_to_query}' AND user_id = {message.from_id}
        ORDER BY date""", conn, parse_dates=['date'])
        await message.answer(df)
    except Exception as e:
        print(e)
        await message.answer(text=f'Ошибка: {e}. Свяжитесь с разработчиком')

# Хендлеры занесения данных в БД
@dp.message_handler(commands=['Спина', 'Грудь', 'Плечи', 'Руки'], state=FSMAutomatic.muscular_group) ## НЕТ НОГ
async def back(message: types.Message, state: FSMContext):
    async with state.proxy() as helping_data:
        helping_data['muscular'] = message.text[1:]
    await message.answer(text=ex_text, reply_markup=dictionary_of_menu[helping_data['muscular']])
    await state.finish()
    await FSMUser.name_of_exs.set()

@dp.message_handler(state=FSMUser.name_of_exs)
async def get_exercise_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_exercise'] = message.text[1:]
    await FSMUser.next()
    await message.reply(text=data_format)

@dp.message_handler(state=FSMUser.data)
async def add_data_to_db(message: types.Message, state: FSMContext):
    """Добавить запись в БД"""
    async with state.proxy() as data:
        data['train_params'] = message.text.split(',')
        data['date'] = date.today()
        data['user_id'] = message.from_id
    await state.finish()
    try:
        # парсинг параметров
        parsed_train_params = '{'
        for i in range(len(data['train_params'])):
            parsed_train_params += data['train_params'][i]
            if i != len(data['train_params']) - 1:
                parsed_train_params += ', '
        parsed_train_params += '}'
        cursor = connection.cursor()
        cursor.execute(f"""
        INSERT INTO exercises_data (user_id, date, exercise, train_params)
        VALUES ({data['user_id']},
                '{data['date']}', 
                {Literal(data['name_exercise']).as_string(cursor)},
                '{parsed_train_params}')""")
        connection.commit()
        cursor.close()
        await message.answer(text=accepted_text, reply_markup=dictionary_of_menu['main_menu'])
    except Exception as e:
        print(e)
        await message.answer(text=f'Ошибка: {e}. Свяжитесь с разработчиком',
                             reply_markup=dictionary_of_menu['muscular_menu'])



executor.start_polling(dp, skip_updates=True)

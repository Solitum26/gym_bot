import prettytable
import pandas as pd
import os
import psycopg2
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from commands_text import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboard import dictionary_of_menu
from datetime import date
from FSM import *
from psycopg2.sql import Literal
from sqlalchemy import create_engine, text
from dotenv import load_dotenv, find_dotenv

def get_connection():
    connenction = psycopg2.connect(
                database='user_data',
                host='localhost',
                user='postgres',
                password=f'{password}')
    return connenction

def validate_exercise_name(text):
    return text in all_exercises

def validate_params(text: str):
    try:
        boolean_flag = ''.join(text.replace('-', ', ').split(', ')).isnumeric()
        return boolean_flag
    except:
        return False

def parsing_data(params_list: list):
    parsed_train_params = '{'
    for i in range(len(params_list)):
        parsed_train_params += params_list[i]
        if i != len(params_list) - 1:
            parsed_train_params += ', '
    parsed_train_params += '}'
    return parsed_train_params

load_dotenv(find_dotenv())
password = os.getenv('password')
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

# Хендлеры занесения данных в БД
@dp.message_handler(commands=['Спина', 'Грудь', 'Плечи', 'Руки'], state=FSMAutomatic.muscular_group) ## НЕТ НОГ
async def automatic_menu(message: types.Message, state: FSMContext):
    """
    Function for automatic determination next menu based on command by user
    """
    async with state.proxy() as helping_data:
        helping_data['muscular'] = message.text[1:]
    await message.answer(text=ex_text, reply_markup=dictionary_of_menu[helping_data['muscular']])
    await state.finish()
    await FSMUser.name_of_exs.set()

@dp.message_handler(commands=all_exercises, state=FSMUser.name_of_exs)
async def get_exercise_name(message: types.Message, state: FSMContext):
    """
    Add to data name of exercise
    """
    async with state.proxy() as data:
        data['name_exercise'] = message.text[1:]
    await FSMUser.next()
    await message.reply(text=data_format)

@dp.message_handler(state=FSMUser.data)
async def add_data_to_db(message: types.Message, state: FSMContext):
    """
    Adding data to PostrgeSQL
    """
    # Валидация
    if not validate_params(message.text):
        await message.answer(text=validate_error_text)
    else:
        async with state.proxy() as data:
            data['train_params'] = message.text.split(', ')
            data['date'] = date.today()
            data['user_id'] = message.from_id
        await state.finish()
        try:
            parsed_train_params = parsing_data(data['train_params'])
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(f"""
            INSERT INTO exercises_data (user_id, date, exercise, train_params)
            VALUES ({data['user_id']},
                    '{data['date']}', 
                    {Literal(data['name_exercise']).as_string(cursor)},
                    '{parsed_train_params}')""")
            connection.commit()
            cursor.close()
            connection.close()
            await message.answer(text=accepted_text, reply_markup=dictionary_of_menu['main_menu'])
        except Exception as e:
            await message.answer(text=f'Ошибка. Свяжитесь с разработчиком',
                                 reply_markup=dictionary_of_menu['muscular_menu'])

# Хендлер отмены действия
@dp.message_handler(state='*', commands='cancel')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply(text='Действие отменено', reply_markup=dictionary_of_menu['main_menu'])

# Хендлер перезаписи ошибчных значнений
@dp.message_handler(commands=['rewrite'])
async def init_state_for_rewriting(message: types.Message):
    """Init 1st state and get data to rewrite"""
    await FSMRewriting.date_and_exercise_to_query.set()
    await message.reply(text=rewriting_text_date)

@dp.message_handler(state=FSMRewriting.date_and_exercise_to_query)
async def get_date_and_exercise_query(message: types.Message, state: FSMContext):
    date_and_exercise = message.text.split()
    if not validate_exercise_name(date_and_exercise[1]):
        await message.answer(text='Неправильное название упражнения')
    else:
        async with state.proxy() as new_data:
            new_data['date'] = date_and_exercise[0][:-1]
            new_data['exercise'] = date_and_exercise[1]
        await FSMRewriting.next()
        await message.reply(text=rewriting_text_new_params)

@dp.message_handler(state=FSMRewriting.new_data_to_update)
async def rewrite_row(message: types.Message, state: FSMContext):
    """Main function for rewriting data"""
    if not validate_params(message.text):
        await message.answer(text=validate_error_text)
    else:
        async with state.proxy() as new_data:
            new_data['new_params'] = message.text.split(', ')
        await state.finish()
        parsed_data = parsing_data(new_data['new_params'])
        try:
            # есть ли в бд записи с заданными параметрами
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(f"""
            SELECT COUNT(*) 
            FROM exercises_data
            WHERE user_id = {message.from_id} AND date = '{new_data['date']}' AND exercise = '{new_data['exercise']}'
            """)
            if cursor.fetchone()[0]:
                connection = get_connection()
                cursor = connection.cursor()
                cursor.execute(f"""
                UPDATE exercises_data
                SET train_params = '{parsed_data}'
                WHERE user_id = {message.from_id} AND date = '{new_data['date']}' AND exercise = '{new_data['exercise']}'""")
                connection.commit()
                cursor.close()
                connection.close()
                await message.reply(text='Данные обновлены', reply_markup=dictionary_of_menu['main_menu'])
            else:
                await message.answer(text='По заданным параметрам нет данных. Проверьте правильность введенных параметров для обновления')
        except Exception as e:
            print(e)
            await message.answer(text=f'Ошибка. Свяжитесь с разработчиком')

# Хендлер просмотра БД
@dp.message_handler(commands=['history'])
async def query(message: types.Message):
    try:
        exercise_to_query = message.text.split()[1]
        if not validate_exercise_name(exercise_to_query):
            await message.answer(text='Неправильное название упражнения')
        else:
            from prettytable import from_db_cursor
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(f"""
            SELECT ROW_NUMBER() OVER() as Номер, date as Дата, array_to_string(train_params, ', ') as Параметры
            FROM exercises_data
            WHERE exercise = '{exercise_to_query}' AND user_id = {message.from_id}
            ORDER BY date""")
            if cursor.rowcount:
                table = from_db_cursor(cursor)
                await message.answer(text=f'```{table}```', parse_mode='Markdown')
            else:
                await message.answer(text='Таблица пуста')
    except IndexError as e:
        await message.answer(text=f'Ошибка. Пожалуйста, введите название упражнения.')
    except Exception as e:
        await message.answer(text='Что-то пошло не так. Перепроверьте запрос или свяжитесь с разработчиком.')

# Получение списка упражнений
@dp.message_handler(commands=['names'])
async def return_names(message: types.Message):
    """Return names of exercises"""
    text_to_answer = ''
    for i in all_exercises:
        text_to_answer += i + '\n'
    await message.answer(text=text_to_answer)


executor.start_polling(dp, skip_updates=True)

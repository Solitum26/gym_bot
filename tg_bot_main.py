import prettytable
import os
import psycopg2
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from commands_text import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboard import dictionary_of_menu_inline
from datetime import date, timedelta
from FSM import *
from psycopg2.sql import Literal
from sqlalchemy import create_engine, text
from dotenv import load_dotenv, find_dotenv
from prettytable import from_db_cursor
import logging

#logging.basicConfig(filename='logs.txt', level=logging.ERROR)

def get_connection():
    connenction = psycopg2.connect(
                database=f'{database}',
                host='localhost',
                user=f'{user}',
                password=f'{password}')
    return connenction

def validate_date(date):
    date_list = date.split('-')
    if len(date_list) != 3:
        return False
    return ''.join(date_list).isnumeric() and 1 <= int(date_list[1]) <= 31 and 1 <= int(date_list[2]) <= 12

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
database = os.getenv('database')
user = os.getenv('user')
password = os.getenv('password')

bot = Bot(os.getenv('TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# начальный экран
@dp.message_handler(commands=['start'])
async def main_menu(message: types.Message):
    await message.answer(text=start_text, reply_markup=dictionary_of_menu_inline['start_menu'])

@dp.callback_query_handler(text='account')
async def user_info(callback: types.CallbackQuery):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(f"""
    SELECT sub_end
    FROM access_table
    WHERE user_id = {callback.from_user.id}""")
    sub_end = cursor.fetchone()
    if sub_end:
        status = 'Активна ✅'
    else:
        status = 'Неактивна ❌'
    if status == 'Активна ✅':
        await callback.message.answer(text=f'⭐ АККАУНТ ⭐ \n\nПодписка: {status}\nДата окончания: {sub_end[0]}',
                                     reply_markup=dictionary_of_menu_inline['account_menu'])
    else:
        await callback.message.answer(text=f'⭐ АККАУНТ ⭐ \n\nПодписка: {status}\n',
                                     reply_markup=dictionary_of_menu_inline['account_menu'])

@dp.callback_query_handler(text='add_probe')
async def add_probe_sub(callback: types.CallbackQuery):
    connection = get_connection()
    cursor = connection.cursor()
    timestamp = timedelta(days=30)
    cursor.execute(f"""
    SELECT probe_sub
    FROM access_table
    WHERE user_id = {callback.from_user.id}""")
    result = cursor.fetchone()
    if result != None and result[0] == 1:
        await callback.message.answer(text='❗ Вы уже воспользовались пробной подпиской')
        return
    try:
        today = date.today()
        connection = get_connection()
        cursor = connection.cursor()
        timestamp = timedelta(days=30)
        cursor.execute(f"""
        INSERT INTO access_table  VALUES ({callback.from_user.id}, '{today}', '{today + timestamp}', {1}) """)
        connection.commit()
        cursor.close()
        connection.close()
        await callback.message.answer(text=f'Подписка на {timestamp.days} дней успешно оформлена!',
                                      reply_markup=dictionary_of_menu_inline['start_menu'])
    except Exception as e:
        print(e)
        await callback.message.answer(text='❌ Ошибка. Вероятно, у вас уже есть активная подписка, проверьте свой аккаунт или свяжитесь с разработчиком')

@dp.callback_query_handler(text='buy')
async def buy_sub(callback: types.CallbackQuery):
    await FSMBuy_sub.product.set()
    await callback.message.answer(text=buy_text, reply_markup=dictionary_of_menu_inline['products'])
"""
@dp.callback_query_handler(text=['first_plan', 'second_plan', 'third_plan'])
async def payment(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as buy_data:
        buy_data['product'] = callback.data
        print(buy_data['product'])
    await state.finish()
"""
# Хендлер окна помощи
@dp.callback_query_handler(text='help')
async def help_message(callback: types.CallbackQuery):
    await callback.message.answer(text=help_text)
    await callback.answer()

# Проверка подписки и вывод меню функций
@dp.callback_query_handler(text='funcs')
async def main(callback: types.CallbackQuery):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(f"""
    SELECT sub_end
    FROM access_table
    WHERE user_id = {callback.from_user.id}""")
    end_sub_date = cursor.fetchone()
    today = date.today()
    if end_sub_date != None and today <= end_sub_date[0]:
        await callback.message.answer(text=main_text, reply_markup=dictionary_of_menu_inline['main_menu'])
    else:
        await callback.message.answer(text='У вас нет активной подписки',
                                      reply_markup=dictionary_of_menu_inline['start_menu'])


# Хендлер новой тренировки
@dp.callback_query_handler(text='Добавить упражнение')
async def type_of_train(callback: types.CallbackQuery, state: FSMContext):
    await FSMAutomatic.muscular_group.set()
    await callback.message.answer(text=add_new_train_text,
                                  reply_markup=dictionary_of_menu_inline['muscular_menu'])
    await callback.answer()

# Хендлеры занесения данных в БД
@dp.callback_query_handler(text=['Спина', 'Грудь', 'Плечи', 'Руки'], state=FSMAutomatic.muscular_group) ## НЕТ НОГ
async def func_for_automatic_menu(callback: types.CallbackQuery, state: FSMContext):
    """
    Function for automatic determination next menu based on command by user
    """
    async with state.proxy() as helping_data:
        helping_data['muscular'] = callback.data
    await callback.message.answer(text=ex_text, reply_markup=dictionary_of_menu_inline[helping_data['muscular']])
    await state.finish()
    await FSMUser.name_of_exs.set()
    await callback.answer()

@dp.callback_query_handler(state=FSMUser.name_of_exs)
async def get_exercise_name(callback: types.CallbackQuery, state: FSMContext):
    """
    Add to data name of exercise
    """
    async with state.proxy() as data:
        data['name_exercise'] = callback.data
    await FSMUser.next()
    if callback.data == 'cancel':
        await cancel_handler(callback, state)
        return
    f_string = callback.data.replace('_', ' ')
    choosen_exercise_text = f'Вы выбрали "{f_string}".' + '\n'
    await callback.message.reply(text=choosen_exercise_text + data_format,
                                 reply_markup=dictionary_of_menu_inline['cancel'])
    await callback.answer()

@dp.message_handler(state=FSMUser.data)
async def add_data_to_db(message: types.Message, state: FSMContext):
    """
    Adding data to PostrgeSQL
    """
    # Валидация
    if not validate_params(message.text):
        await message.answer(text=validate_error_text)
        return
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
        await message.answer(text=accepted_text, reply_markup=dictionary_of_menu_inline['main_menu'])
    except Exception as e:
        print(e)
        await message.answer(text=f'Ошибка. Свяжитесь с разработчиком',
                             reply_markup=dictionary_of_menu_inline['muscular_menu'])

# Хендлер отмены действия
@dp.callback_query_handler(text='cancel', state='*')
async def cancel_handler(callback: types.CallbackQuery, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await callback.message.reply(text='✔️ Действие отменено')
    await callback.message.answer(text=start_text, reply_markup=dictionary_of_menu_inline['start_menu'])
    await callback.answer()

# Хендлер перезаписи ошибчных значнений
@dp.callback_query_handler(text='rewrite')
async def init_state_for_rewriting(callback: types.CallbackQuery):
    """Init 1st state and get data to rewrite"""
    await FSMRewriting.date_to_rewrite.set()
    await callback.message.reply(text=rewriting_text_date, reply_markup=dictionary_of_menu_inline['cancel'])
    await callback.answer()

@dp.message_handler(state=FSMRewriting.date_to_rewrite)
async def get_exercise_query(message: types.Message, state: FSMContext):
    if not validate_date(message.text):
        await message.answer(text='❗ Не пройдена валидация. Пожалуйста, введите корректную дату.')
        return
    async with state.proxy() as new_data:
        new_data['date'] = message.text
    await FSMRewriting.next()
    await message.answer(text='Выберите упражнение:', reply_markup=dictionary_of_menu_inline['all_ex'])

@dp.callback_query_handler(state=FSMRewriting.exercise_to_rewrite)
async def get_exercise(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as new_data:
        new_data['exercise'] = callback.data
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(f"""
    SELECT COUNT(user_id) as count_rows
    FROM exercises_data
    WHERE user_id = {callback.from_user.id} 
    AND date = '{new_data['date']}' 
    AND exercise = '{new_data['exercise']}'""")
    date = new_data['date']
    exercise = new_data['exercise'].replace('_', ' ')
    if not cursor.fetchone()[0]:
        await callback.message.answer(text=f'❗ По дате {date} и упражнению {exercise} нет записей. Попробуйте ввести другие данные.')
        await callback.answer()
        return
    await FSMRewriting.next()

    await callback.message.answer(text='Вы собираетесь обновить запись: \n' +
                                       f'📅 Дата - {date} \n' +
                                       f'🏋️‍♂️ Упражнение - {exercise}', reply_markup=dictionary_of_menu_inline['ok'])
    await callback.answer()

@dp.callback_query_handler(text='ok', state=FSMRewriting.ok_state)
async def exercise(callback: types.CallbackQuery):
    await callback.message.answer(text=rewriting_text_new_params)
    await FSMRewriting.next()

@dp.message_handler(state=FSMRewriting.new_data_to_update)
async def rewrite_row(message: types.Message, state: FSMContext):
    """Main function for rewriting data"""
    if not validate_params(message.text):
        await message.answer(text=validate_error_text)
        return
    async with state.proxy() as new_data:
        new_data['new_params'] = message.text.split(', ')
    await state.finish()
    parsed_data = parsing_data(new_data['new_params'])
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(f"""
        UPDATE exercises_data
        SET train_params = '{parsed_data}'
        WHERE user_id = {message.from_id} 
        AND date = '{new_data['date']}' 
        AND exercise = '{new_data['exercise']}'""")
        connection.commit()
        cursor.close()
        connection.close()
        await message.reply(text='✔️ Данные обновлены!', reply_markup=dictionary_of_menu_inline['main_menu'])
    except Exception as e:
        print(e)
        await message.answer(text=f'❌ Ошибка. Свяжитесь с разработчиком')

# Хендлер просмотра БД
@dp.callback_query_handler(text='history')
async def get_exercise(callback: types.CallbackQuery):
    await FSHHistory.exercises_to_query.set()
    await callback.message.reply(text='Выберите упражнение, по которому будет осуществлен запрос к БД:',
                                 reply_markup=dictionary_of_menu_inline['all_ex'])
    await callback.answer()

@dp.callback_query_handler(state=FSHHistory.exercises_to_query)
async def query(callback: types.CallbackQuery, state: FSMContext):
    try:
        exercise_to_query = callback.data
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(f"""
        SELECT ROW_NUMBER() OVER() as Номер, date as Дата, array_to_string(train_params, ', ') as Параметры
        FROM exercises_data
        WHERE exercise = '{callback.data}' AND user_id = {callback.from_user.id}
        ORDER BY date""")
        choosen_ex = callback.data.replace('_', ' ')
        if cursor.rowcount:
            table = from_db_cursor(cursor)
            await callback.message.answer(text=f'Таблица по {choosen_ex}: \n\n'f'```{table}```', parse_mode='Markdown')
            await callback.message.answer(text=main_text,
                                          reply_markup=dictionary_of_menu_inline['main_menu'])
            await state.finish()
            await callback.answer()
        else:
            await callback.message.answer(text=f'❗В базе данных нет записей по упражнению {choosen_ex}; результирующая таблица пуста.')
            await callback.answer()
    except Exception as e:
        await state.finish()
        print(e)
        await callback.message.answer(text='❌ Что-то пошло не так. Перепроверьте запрос или свяжитесь с разработчиком.',
                                      reply_markup=dictionary_of_menu_inline['main_menu'])



executor.start_polling(dp, skip_updates=True)

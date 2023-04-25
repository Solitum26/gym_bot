import asyncio
import os
import random
import pandas as pd
import psycopg2
from contextlib import suppress
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.exceptions import MessageNotModified
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from commands_text import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboard import dictionary_of_menu_inline, cancel_button
from datetime import date, timedelta
from FSM import *
from psycopg2.sql import Literal
from dotenv import load_dotenv, find_dotenv
from prettytable import from_db_cursor


def get_connection():
    connection = psycopg2.connect(
                database=f'{database}',
                host='localhost',
                user=f'{user}',
                password=f'{password}')
    return connection


def validate_date(date_string):
    date_list = date_string.split('-')
    if len(date_list) != 3:
        return False
    return ''.join(date_list).isnumeric() and '01' <= date_list[1] <= '12' and '01' <= date_list[2] <= '31'


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


def new_kb(level):
    new_kb_ = InlineKeyboardMarkup(row_width=1)
    level = level
    for k in all_exercises[level]:
        new_button = InlineKeyboardButton(text=k.replace('_', ' '), callback_data=k)
        new_kb_.add(new_button)
    new_kb_.add(cancel_button)
    if 0 < level < len(all_exercises) - 1:
        prev = InlineKeyboardButton(text='<<', callback_data='<<')
        next_ = InlineKeyboardButton(text='>>', callback_data='>>')
        new_kb_.row(prev, next_)
    elif level == 0:
        next_ = InlineKeyboardButton(text='>>', callback_data='>>')
        new_kb_.add(next_)
    elif level == len(all_exercises) - 1:
        prev = InlineKeyboardButton(text='<<', callback_data='<<')
        new_kb_.add(prev)
    return new_kb_


load_dotenv(find_dotenv())
database = os.getenv('database')
user = os.getenv('user')
password = os.getenv('password')
loop_bot = asyncio.new_event_loop()
bot = Bot(os.getenv('TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
loop_admin_bot = asyncio.new_event_loop()
admin_bot = Bot(os.getenv('ADMIN_BOT'))
dp_admin = Dispatcher(admin_bot, loop=loop_admin_bot)


@dp.message_handler(commands=['create_promo'])
async def create_promo(message: types.Message):
    if message.from_id == 779123467:
        from string import ascii_letters, digits
        import random
        new_promocode = '!' + ''.join(random.sample(ascii_letters + digits, k=8))
        promocodes[new_promocode] = message.text.split()[1]
        await message.answer(text=f'Новый промокод - {new_promocode}')
        result = ''
        for key, value in promocodes.items():
            result += f'{key} - {value} дней' + '\n'
        await message.answer(text=f'Список существующих:\n{result}')


@dp.message_handler(Text(startswith='!'))
async def get_promo(message: types.Message):
    if message.text in promocodes:
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(f"""
            SELECT sub_end
            FROM access_data
            WHERE user_id = {message.from_id}""")
            end_sub = cursor.fetchone()
            timestamp = timedelta(days=int(promocodes[message.text]))
            if end_sub:
                new_sub_end = end_sub[0] + timestamp
                cursor.execute(f"""
                            UPDATE access_data
                            SET sub_end = '{new_sub_end}'
                            WHERE user_id = {message.from_id}""")
                connection.commit()
            else:
                new_sub_end = date.today() + timestamp
                cursor.execute(f"""
                INSERT INTO access_data VALUES ({message.from_id}, '{date.today()}', '{new_sub_end}')""")
                connection.commit()
            cursor.close()
            connection.close()
            await message.answer(text='Промокод применен!', reply_markup=dictionary_of_menu_inline['start_menu'])
        except Exception as e:
            print(e)
            await message.answer(text='Непредвиденная ошибка')
        finally:
            promocodes.pop(message.text)
    else:
        await message.answer(text='Промокод не существует', reply_markup=dictionary_of_menu_inline['start_menu'])


@dp.message_handler(commands=['query'])
async def admin_query(message: types.Message):
    if message.from_id == 779123467:
        try:
            if '@' in message.text:
                connection = get_connection()
                cursor = connection.cursor()
                cursor.execute(f"""{message.text.split('@')[-1]}""")
                connection.commit()
                cursor.close()
                connection.close()
                await message.answer(text='Успешно')
            elif '#' in message.text:
                connection = get_connection()
                cursor = connection.cursor()
                cursor.execute(f"""{message.text.split('#')[-1].strip()}""")
                result = cursor.fetchall()
                t = pd.DataFrame(result)
                await message.answer(text=f'```{t}```', parse_mode='Markdown')
        except Exception as e:
            print(e)
            await message.answer(text='Ошибка БД')
    else:
        await message.answer(text='Нет доступа')


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
    FROM access_data
    WHERE user_id = {callback.from_user.id}""")
    sub_end = cursor.fetchone()
    if sub_end:
        status = '✅ Активна'
        await callback.message.answer(text=f'⭐ АККАУНТ ⭐ \n\nПодписка: {status}\nДата окончания: {sub_end[0]}',
                                      reply_markup=dictionary_of_menu_inline['account_menu'])
    else:
        status = '❌ Неактивна'
        await callback.message.answer(text=f'⭐ АККАУНТ ⭐ \n\nПодписка: {status}\n',
                                      reply_markup=dictionary_of_menu_inline['account_menu'])
    cursor.close()
    connection.close()
    await callback.answer()


@dp.callback_query_handler(text='add_probe')
async def add_probe_sub(callback: types.CallbackQuery):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(f"""
    SELECT sub_end, probe_sub
    FROM access_data
    WHERE user_id = {callback.from_user.id}""")
    result = cursor.fetchone()
    if result is None:
        try:
            today = date.today()
            connection = get_connection()
            cursor = connection.cursor()
            timestamp = timedelta(days=30)
            cursor.execute(f"""
            INSERT INTO access_data VALUES ({callback.from_user.id}, '{today}', '{today + timestamp}', {1}) """)
            connection.commit()
            cursor.close()
            connection.close()
            await callback.message.answer(text=f'Подписка на {timestamp.days} дней успешно оформлена!',
                                          reply_markup=dictionary_of_menu_inline['start_menu'])
        except Exception as e:
            print(e)
            await callback.message.answer(
                text='❌ Ошибка. Вероятно, у вас уже есть активная подписка, проверьте свой аккаунт или свяжитесь с разработчиком')
    elif result[1] == 0:
        try:
            today = date.today()
            connection = get_connection()
            cursor = connection.cursor()
            timestamp = timedelta(days=30)
            cursor.execute(f"""
            UPDATE access_data
            SET (sub_start, sub_end, probe_sub) = ('{today}', '{result[0] + timestamp}', {1})
            WHERE user_id = {callback.from_user.id}""")
            connection.commit()
            cursor.close()
            connection.close()
            await callback.message.answer(text=f'Подписка на {timestamp.days} дней успешно оформлена!',
                                          reply_markup=dictionary_of_menu_inline['start_menu'])
        except Exception as e:
            print(e)
            await callback.message.answer(
                text='❌ Ошибка. Вероятно, у вас уже есть активная подписка, проверьте свой аккаунт или свяжитесь с разработчиком')
    else:
        await callback.message.answer(text='❗ Вы уже воспользовались пробной подпиской')
        await callback.answer()
        return
    await callback.answer()


@dp.callback_query_handler(text='buy')
async def buy_sub(callback: types.CallbackQuery):
    await BuySub.buying_state.set()
    await callback.message.answer(text=products_text, reply_markup=dictionary_of_menu_inline['products'])
    await callback.answer()


@dp.callback_query_handler(text=['30', '60', '90'], state=BuySub.buying_state)
async def payment(callback: types.CallbackQuery, state: FSMContext):
    user_id = int(callback.from_user.id)
    kostil[user_id] = {}
    plan = callback.data
    kostil[user_id]['plan'] = callback.data
    chat_id = callback.message.chat.id
    kb_test = InlineKeyboardMarkup(row_width=1)
    accept_button = InlineKeyboardButton(text=f'Принять',
                                         callback_data=f'give_sub {user_id} {callback.data} {chat_id}')
    decline_button = InlineKeyboardButton(text='Отклонить', callback_data=f'decline_sub {chat_id} {user_id}')
    kb_test.add(accept_button, decline_button)
    dict_of_kb_status[user_id] = {'kb': kb_test}
    await callback.message.answer(text=f'Выбрано: {callback.data} дней\nСтоимость: {dict_of_price[callback.data]}\n' + buy_text,
                                  reply_markup=dictionary_of_menu_inline['cancel'])
    await callback.answer()
    await BuySub.next()


@dp.message_handler(content_types=types.ContentType.PHOTO, state=BuySub.photo)
async def get_photo(message: types.Message, state: FSMContext):
    await message.answer(text=wait_status_sub)
    user_name = '@' + message.chat.username
    user_id = message.from_id
    await bot.send_message(chat_id=779123467,
                           text=f'⚡ НОВЫЙ ПЛАТЕЖ ⚡\nПользователь -  {user_name}\nПродукт - {kostil[user_id]["plan"]} дней')
    kostil[message.from_id]['message_id'] = message.message_id
    await message.send_copy(chat_id=779123467, reply_markup=dict_of_kb_status[user_id]['kb'])
    await state.finish()
    with suppress(MessageNotModified):
        for k in range(1000):
            if kostil[message.from_id].get('clock'):
                kostil.pop(user_id)
                break
            await asyncio.sleep(4)
            j = 0
            for i in clocks:
                await asyncio.sleep(1.2)
                await bot.edit_message_text(text=wait_status_sub + '\n' + '- ' * 35 + f'\n{i} Получение статуса платежа' + '......'[:j],
                                            chat_id=message.chat.id, message_id=message.message_id + 1)
                if j == 6:
                    j = 0
                if kostil[int(message.from_id)].get('clock'):
                    await bot.edit_message_text(
                        text=wait_status_sub + '\n' + '- ' * 35 + f'\nОбработка завершена! ✅',
                        chat_id=message.chat.id, message_id=message.message_id + 1)
                    break
                j += 1


@dp.callback_query_handler(Text(contains="give_sub"))
async def give_sub_to_user(callback: types.CallbackQuery):
    parsed_callback = callback.data.split()
    user_id = int(parsed_callback[1])
    plan = parsed_callback[2]
    chat_id = parsed_callback[3]
    kostil[user_id]['clock'] = 1
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(f"""
        SELECT count(*)
        FROM access_data
        WHERE user_id = {user_id}""")
        result = cursor.fetchone()[0]
        timestamp = timedelta(days=int(plan))
        if result:
            cursor.execute(f"""
            UPDATE access_data
            SET sub_end = (SELECT sub_end FROM access_data WHERE user_id = {user_id}) + {timestamp.days}
            WHERE user_id = {user_id}
            """)
            connection.commit()
        else:
            cursor.execute(f"""
            INSERT INTO access_data VALUES ({user_id}, '{date.today()}', '{date.today() + timestamp}')
                        """)
            connection.commit()
        cursor.close()
        connection.close()
        await bot.send_message(chat_id=chat_id, text=sub_accepted_text,
                               reply_markup=dictionary_of_menu_inline['start_menu'])
    except Exception as e:
        print(e)
    await callback.message.delete()
    await callback.message.answer(text='⬆️ Статус: принято')
    await callback.answer()


@dp.callback_query_handler(Text(contains='decline_sub'))
async def decline_user_sub(callback: types.CallbackQuery):
    await callback.message.delete()
    chat_id = int(callback.data.split()[1])
    user_id = int(callback.data.split()[2])
    kostil[user_id]['clock'] = 1
    await bot.send_message(chat_id=chat_id, text=sub_declined_text,
                           reply_markup=dictionary_of_menu_inline['start_menu'])
    await callback.message.answer(text='⬆️ Статус: отклонен')
    await callback.answer()


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
    FROM access_data
    WHERE user_id = {callback.from_user.id}""")
    end_sub_date = cursor.fetchone()
    today = date.today()
    if end_sub_date is not None and today <= end_sub_date[0]:
        await callback.message.answer(text=main_text, reply_markup=dictionary_of_menu_inline['main_menu'])
    else:
        await callback.message.answer(text='У вас нет активной подписки',
                                      reply_markup=dictionary_of_menu_inline['start_menu'])
    await callback.answer()


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
    await callback.message.reply(text='✅ Действие отменено')
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
    kb = new_kb(0)
    pages[message.from_id] = {}
    pages[message.from_id]['level'] = 0
    await message.answer(text='Выберите упражнение:', reply_markup=kb)


@dp.callback_query_handler(text=all_ex, state=FSMRewriting.exercise_to_rewrite)
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
        await callback.message.answer(text=f'❗ По дате {date} и упражнению {exercise} нет записей. Попробуйте выбрать другие данные.')
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
        await message.reply(text='✅ Данные обновлены!', reply_markup=dictionary_of_menu_inline['main_menu'])
    except Exception as e:
        print(e)
        await message.answer(text=f'❌ Ошибка. Свяжитесь с разработчиком')


@dp.callback_query_handler(text=['<<', '>>'], state=[FSHHistory.exercises_to_query, FSMRewriting.exercise_to_rewrite])
async def paging(callback: types.CallbackQuery):
    if callback.data == '>>':
        pages[callback.from_user.id]['level'] += 1
        kb = new_kb(pages[callback.from_user.id]['level'])
        with suppress(MessageNotModified):
            await callback.message.edit_reply_markup(reply_markup=kb)
    if callback.data == '<<':
        pages[callback.from_user.id]['level'] -= 1
        kb = new_kb(pages[callback.from_user.id]['level'])
        with suppress(MessageNotModified):
            await callback.message.edit_reply_markup(reply_markup=kb)


# Хендлер просмотра БД
@dp.callback_query_handler(text=['history'])
async def get_exercise(callback: types.CallbackQuery):
    pages[callback.from_user.id] = {}
    pages[callback.from_user.id]['level'] = 0
    if callback.data == 'history':
        kb = new_kb(0)
        await callback.message.reply(text='Выберите упражнение, по которому будет осуществлен запрос к БД:',
                                     reply_markup=kb)
    await callback.answer()
    await FSHHistory.exercises_to_query.set()


@dp.callback_query_handler(text=all_ex, state=FSHHistory.exercises_to_query)
async def query(callback: types.CallbackQuery, state: FSMContext):

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(f"""
        SELECT ROW_NUMBER() OVER() as Номер, date as Дата, array_to_string(train_params, ', ') as Параметры
        FROM exercises_data
        WHERE exercise = '{callback.data}' AND user_id = {callback.from_user.id}
        ORDER BY date""")
        chosen_ex = callback.data.replace('_', ' ')
        if cursor.rowcount:
            table = from_db_cursor(cursor)
            await callback.message.answer(text=f'Таблица по {chosen_ex}: \n\n'f'```{table}```', parse_mode='Markdown')
            await callback.message.answer(text=main_text,
                                          reply_markup=dictionary_of_menu_inline['main_menu'])
            await state.finish()
            await callback.answer()
            pages.pop(callback.from_user.id)
        else:
            await callback.message.answer(text=f'❗ В базе данных нет записей по упражнению {chosen_ex}; результирующая таблица пуста.')
            await callback.answer()
    except Exception as e:
        await state.finish()
        print(e)
        await callback.message.answer(text='❌ Что-то пошло не так. Перепроверьте запрос или свяжитесь с разработчиком.',
                                      reply_markup=dictionary_of_menu_inline['main_menu'])


#asyncio.gather(*[executor.start_polling(dp, skip_updates=True), executor.start_polling(dp_admin, skip_updates=False)])
executor.start_polling(dp, skip_updates=True)


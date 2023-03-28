from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from commands_text import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboard import dictionary_of_menu
from exercises import  *
from datetime import date
from FSM import FSMUser, FSMContext
from connect_to_SQL import connection
from psycopg2.sql import Literal

cursor = connection.cursor()
TOKEN = '6284880447:AAHj24KgUb7NdxES-aIhXqOerghNbsw6cwM'
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

# начальный экран
@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.answer(text=start_text, reply_markup=dictionary_of_menu['main_menu'])

@dp.message_handler(commands=['help'])
async def start_message(message: types.Message):
    await message.answer(text=help_text)

# выбор тренировки

@dp.message_handler(commands=['new_train'])
async def type_of_train(message):
    await message.answer(text=add_new_train_text, reply_markup=dictionary_of_menu['muscular_menu'])

# Хендлер спины и упражнений на спину
@dp.message_handler(commands=['Спина'])
async def back(message):
    await message.answer(text=ex_text, reply_markup=dictionary_of_menu['back_menu'])
    await FSMUser.name_of_exs.set()

@dp.message_handler(commands=back_ex, state=FSMUser.name_of_exs)
async def f(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_exercise'] = str(message.text[1:])
    await FSMUser.next()
    await message.reply(text=data_format)

@dp.message_handler(state=FSMUser.data)
async def add_data_to_db(message: types.Message, state: FSMContext):
    today = date.today()
    async with state.proxy() as data:
        data['train_params'] = message.text.split(',')
        data['date'] = today
        data['user_id'] = message.from_id
    await state.finish()
    try:
        parsed_train_params = '{'
        for i in range(len(data['train_params'])):
            parsed_train_params += data['train_params'][i]
            if i != len(data['train_params']) - 1:
                parsed_train_params += ', '
        parsed_train_params += '}'
        print(parsed_train_params)
        print(data['date'])
        cursor.execute(f"""
        INSERT INTO back_data (user_id, date, exercise, train_params)
        VALUES ({data['user_id']},
                '{data['date']}', 
                {Literal(data['name_exercise']).as_string(cursor)},
           :     {f})""")
        await message.answer(text=accepted_text, reply_markup=dictionary_of_menu['main_menu'])
        cursor.close()
    except Exception as e:
        print(e)
        await message.answer(text='Ошибка')



executor.start_polling(dp, skip_updates=True)

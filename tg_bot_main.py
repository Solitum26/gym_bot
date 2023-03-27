from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from commands_text import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboard import dictionary_of_menu
from exercises import  *
from datetime import date
from FSM import FSMUser, FSMContext


TOKEN = '6284880447:AAHj24KgUb7NdxES-aIhXqOerghNbsw6cwM'
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.answer(text=start_text, reply_markup=dictionary_of_menu['main_menu'])

@dp.message_handler(commands=['help'])
async def start_message(message: types.Message):
    await message.answer(text=help_text)

@dp.message_handler(commands=['new_train'])
async def type_of_train(message):
    await message.answer(text=add_new_train_text, reply_markup=dictionary_of_menu['muscular_menu'])

@dp.message_handler(commands=['Спина'])
async def back(message):
    await message.answer(text=ex_text, reply_markup=dictionary_of_menu['back_menu'])

@dp.message_handler(commands=back_ex, state=None)
async def f(message: types.Message):
    await FSMUser.data.set()
    await message.reply(text=data_format)

@dp.message_handler(state=FSMUser.data)
async def g(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data[str(date.today())] = message.text.split(',')
        print(data)



executor.start_polling(dp, skip_updates=True)

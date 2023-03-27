from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup



# стартовое меню
mainmenu_help = KeyboardButton('/help')
mainmenu_train = KeyboardButton('/new_train')

main_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
                                .row(mainmenu_train,
                                     mainmenu_help)

# меню выбора целевой группы
muscular_menu_chest = KeyboardButton('/Грудь')
muscular_menu_arms = KeyboardButton('/Руки')
muscular_menu_shoulders = KeyboardButton('/Плечи')
muscular_menu_legs = KeyboardButton('/Ноги')
muscular_menu_back = KeyboardButton('/Спина')

list_of_muscular = [muscular_menu_back,
                    muscular_menu_legs,
                    muscular_menu_shoulders,
                    muscular_menu_arms,
                    muscular_menu_chest]

muscular_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
                .row(*list_of_muscular)

# меню упражнений спина
back_ex_1 = KeyboardButton('/Тяга_верхного_блока')
back_ex_2 = KeyboardButton('/Тяга_горизонтального_блока')
back_ex_3 = KeyboardButton('/Пуловер')
back_ex_4 = KeyboardButton('/Тяга_гантели_к_поясу')
back_ex_5 = KeyboardButton('/Т-гриф')

list_of_back = [back_ex_1, back_ex_2, back_ex_3, back_ex_4, back_ex_5]
back_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
                                .row(*list_of_back)

dictionary_of_menu = {'main_menu': main_menu,
                      'muscular_menu': muscular_menu,
                      'back_menu': back_menu}


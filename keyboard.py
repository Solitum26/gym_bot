from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup



# стартовое меню
mainmenu_help = KeyboardButton('/help')
mainmenu_train = KeyboardButton('/new_train')
mainmenu_query = KeyboardButton('/check_history')

list_of_mainmenu = [mainmenu_query,
                    mainmenu_help,
                    mainmenu_train]

main_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
                                .row(*list_of_mainmenu)

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

list_of_back = [back_ex_1,
                back_ex_2,
                back_ex_3,
                back_ex_4,
                back_ex_5]

back_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
                                .row(*list_of_back)
# меню упражнений грудь
chest_ex_1 = KeyboardButton('/Жим_лежа_горизонтальный_гриф')
chest_ex_2 = KeyboardButton('/Жим_лежа_горизонтальный_гантели')
chest_ex_3 = KeyboardButton('/Изоляция')
chest_ex_4 = KeyboardButton('/Жим_Свенда')
chest_ex_5 = KeyboardButton('/Брусья_отжимания')

list_of_chest = [chest_ex_5,
                 chest_ex_4,
                 chest_ex_3,
                 chest_ex_2,
                 chest_ex_1]

chest_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
                                .row(*list_of_chest)


# меню упражнений плечи
shoulders_ex_1 = KeyboardButton('/Махи_средняя')
shoulders_ex_2 = KeyboardButton('/Махи_передняя')
shoulders_ex_3 = KeyboardButton('/Махи_задняя')
shoulders_ex_4 = KeyboardButton('/Протяжка')
shoulders_ex_5 = KeyboardButton('/Жим_гантелей')

list_of_shoulders = [shoulders_ex_5,
                     shoulders_ex_4,
                     shoulders_ex_3,
                     shoulders_ex_2,
                     shoulders_ex_1]

shoulders_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
                                    .row(*list_of_shoulders)

# меню упражнений руки

arms_ex_1 = KeyboardButton('/Французский_жим')
arms_ex_2 = KeyboardButton('/Трицепс_канат')
arms_ex_3 = KeyboardButton('/Скамья_Скота')
arms_ex_4 = KeyboardButton('/Бицепс_сгибания_рук')

list_of_arms = [arms_ex_4,
                arms_ex_3,
                arms_ex_2,
                arms_ex_1]

arms_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
                                .row(*list_of_arms)

dictionary_of_menu = {'main_menu': main_menu,
                      'muscular_menu': muscular_menu,
                      'Спина': back_menu,
                      'Грудь': chest_menu,
                      'Руки': arms_menu,
                      'Плечи': shoulders_menu}
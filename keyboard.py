from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup
from commands_text import all_exercises

cancel_button = InlineKeyboardButton(text='🚫 Отменить действие', callback_data='cancel')

# Стартовое меню
start_menu = InlineKeyboardMarkup(row_width=1)
account_button = InlineKeyboardButton(text='🪪 Мой аккаунт', callback_data='account')
main_funcs_button = InlineKeyboardButton(text='⚙️ Основные функции', callback_data='funcs')
mainmenu_help_inline = InlineKeyboardButton(text='❓ Помощь', callback_data='help')
start_menu_buttons = [account_button, main_funcs_button, mainmenu_help_inline]
start_menu.add(*start_menu_buttons)

# Аккаунт
account_menu = InlineKeyboardMarkup(row_width=1)
probe_button = InlineKeyboardButton(text='🆓 Пробный период', callback_data='add_probe')
buy_sub = InlineKeyboardButton(text='💲 Приобрести подписку', callback_data='buy')
account_menu.add(probe_button, buy_sub)

# Главное меню
main_menu_inline = InlineKeyboardMarkup(row_width=1)
mainmenu_train_inline = InlineKeyboardButton(text='🏋️‍♂️ Добавить упражнение', callback_data='Добавить упражнение')
mainmenu_rewrite_inline = InlineKeyboardButton(text='✍🏻 Перезаписать значение', callback_data='rewrite')
mainmenu_history_inline = InlineKeyboardButton(text='👁️‍ Просмотреть данные', callback_data='history')

list_of_mainmenu_2 = [mainmenu_train_inline, mainmenu_rewrite_inline, mainmenu_history_inline]

main_menu_inline.add(*list_of_mainmenu_2)

# Выбор группы
muscular_menu_inline = InlineKeyboardMarkup(row_width=1)
muscular_menu_chest_inline = InlineKeyboardButton(text='Грудь', callback_data='Грудь')
muscular_menu_arms_inline = InlineKeyboardButton(text='Руки', callback_data='Руки')
muscular_menu_shoulders_inline = InlineKeyboardButton(text='Плечи', callback_data='Плечи')
muscular_menu_legs_inline = InlineKeyboardButton(text='Ноги', callback_data='Ноги')
muscular_menu_back_inline = InlineKeyboardButton(text='Спина', callback_data='Спина')

list_of_muscular_menu_inline = [muscular_menu_chest_inline,
                                muscular_menu_back_inline,
                                muscular_menu_shoulders_inline,
                                muscular_menu_arms_inline,
                                cancel_button]

muscular_menu_inline.add(*list_of_muscular_menu_inline)

# Упражнения спина
back_ex_1_in = InlineKeyboardButton(text='Тяга вертикального блока', callback_data='Тяга_вертикального_блока')
back_ex_2_in = InlineKeyboardButton(text='Тяга горизонтального блока', callback_data='Тяга_горизонтального_блока')
back_ex_3_in = InlineKeyboardButton(text='Пуловер', callback_data='Пуловер')
back_ex_4_in = InlineKeyboardButton(text='Тяга гантели к поясу', callback_data='Тяга_гантели_к_поясу')
back_ex_5_in = InlineKeyboardButton(text='Т-гриф', callback_data='Т-гриф')

list_of_back_in = [back_ex_1_in,
                   back_ex_2_in,
                   back_ex_3_in,
                   back_ex_4_in,
                   back_ex_5_in,
                   cancel_button]

back_menu_in = InlineKeyboardMarkup(row_width=1) \
                                   .add(*list_of_back_in)

# Упражнения грудь
chest_ex_1_in = InlineKeyboardButton(text='Жим лежа горизонтальный гриф', callback_data='Жим_лежа_горизонтальный_гриф')
chest_ex_2_in = InlineKeyboardButton(text='Жим лежа горизонтальный гантели', callback_data='Жим_лежа_горизонтальный_гантели')
chest_ex_3_in = InlineKeyboardButton(text='Изоляция грудь', callback_data='Изоляция_грудь')
chest_ex_4_in = InlineKeyboardButton(text='Жим Cвенда', callback_data='Жим_Свенда')
chest_ex_5_in = InlineKeyboardButton(text='Брусья отжимания', callback_data='Брусья_отжимания')
chest_ex_6_in = InlineKeyboardButton(text='Жим гантелей под углом', callback_data='Жим_гантелей_под_углом')

list_of_chest_in = [chest_ex_5_in,
                    chest_ex_4_in,
                    chest_ex_3_in,
                    chest_ex_2_in,
                    chest_ex_1_in,
                    chest_ex_6_in,
                    cancel_button]

chest_menu_in = InlineKeyboardMarkup(row_width=1) \
                                    .add(*list_of_chest_in)
# Меню упражнений плечи
shoulders_ex_1_in = InlineKeyboardButton(text='Махи средняя', callback_data='Махи_средняя')
shoulders_ex_2_in = InlineKeyboardButton(text='Махи передняя', callback_data='Махи_передняя')
shoulders_ex_3_in = InlineKeyboardButton(text='Махи задняя', callback_data='Махи_задняя')
shoulders_ex_4_in = InlineKeyboardButton(text='Протяжка', callback_data='Протяжка')
shoulders_ex_5_in = InlineKeyboardButton(text='Жим гантелей', callback_data='Жим_гантелей')

list_of_shoulders_in = [shoulders_ex_5_in,
                        shoulders_ex_4_in,
                        shoulders_ex_3_in,
                        shoulders_ex_2_in,
                        shoulders_ex_1_in,
                        cancel_button]

shoulders_menu_in = InlineKeyboardMarkup(row_width=1) \
                                        .add(*list_of_shoulders_in)

# меню упражнений руки

arms_ex_1_in = InlineKeyboardButton(text='Французский жим', callback_data='Французский_жим')
arms_ex_2_in = InlineKeyboardButton(text='Трицепс в смите канат', callback_data='Трицепс_в_смите_канат')
arms_ex_3_in = InlineKeyboardButton(text='Скамья Скота', callback_data='Скамья_Скота')
arms_ex_4_in = InlineKeyboardButton(text='Бицепс сгибания рук', callback_data='Бицепс_сгибания_рук')

list_of_arms_in = [arms_ex_4_in,
                   arms_ex_3_in,
                   arms_ex_2_in,
                   arms_ex_1_in,
                   cancel_button]

arms_menu_in = InlineKeyboardMarkup(row_width=1) \
                                .add(*list_of_arms_in)


# Меню отмены

cancel_kb = InlineKeyboardMarkup(row_width=1) \
                                .add(cancel_button)

# меню всех упражнений
all_exercises_menu = InlineKeyboardMarkup(row_width=3)
for i in all_exercises:
    name = i.replace('_', ' ')
    button = InlineKeyboardButton(text=name, callback_data=i)
    all_exercises_menu.add(button)

all_exercises_menu.add(cancel_button)
# подтверждение перезаписи

ok_button = InlineKeyboardButton(text='ОК', callback_data='ok')
ok = InlineKeyboardMarkup(row_width=1).add(ok_button, cancel_button)

# Покупка
products = InlineKeyboardMarkup(row_width=1)
sub_button_three = InlineKeyboardButton(text='30 дней', callback_data='first_plan')
sub_button_six = InlineKeyboardButton(text='60 дней', callback_data='second_plan')
sub_button_nine = InlineKeyboardButton(text='90 дней', callback_data='third_plan')

products.add(sub_button_three, sub_button_six, sub_button_nine, cancel_button)

dictionary_of_menu_inline = {'start_menu': start_menu,
                             'main_menu': main_menu_inline,
                             'muscular_menu': muscular_menu_inline,
                             'Спина': back_menu_in,
                             'Грудь': chest_menu_in,
                             'Руки': arms_menu_in,
                             'Плечи': shoulders_menu_in,
                             'cancel': cancel_kb,
                             'all_ex': all_exercises_menu,
                             'ok': ok,
                             'account_menu': account_menu,
                             'products': products}

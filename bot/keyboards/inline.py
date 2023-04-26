from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_menu_ikb():
    menu_ikb = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text= "Розрахувати",
                                   callback_data="calculate")
    button2 = InlineKeyboardButton(text= "Допомога",
                                   callback_data="help")
    button3 = InlineKeyboardButton(text= "Відписатись",
                                   callback_data="unsub")
    button4 = InlineKeyboardButton(text= "Фідбек",
                                   callback_data="feedback")
    menu_ikb.add(button1,button2,button3,button4)
    return menu_ikb

def get_unsub_ikb():
    unsub_ikb = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text= "Так",
                                   callback_data="yes")
    button2 = InlineKeyboardButton(text= "Ні",
                                   callback_data="no")

    unsub_ikb.add(button1,button2)
    return unsub_ikb

def get_feedback_ikb():
    feedback_ikb = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(text="Відмінити",
                                   callback_data="out")
    feedback_ikb.add(button1)
    return feedback_ikb

def get_add_subj_ikb():
    add_subj_ikb = InlineKeyboardMarkup(row_width=2)

    ib1 = InlineKeyboardButton(text="Іноземна мова",
                               callback_data='english')
    ib2 = InlineKeyboardButton(text="Фізика",
                               callback_data='physics')
    ib3 = InlineKeyboardButton(text="Хімія",
                               callback_data='chemistry')
    ib4 = InlineKeyboardButton(text="Біологія",
                               callback_data='biology')
    ib5 = InlineKeyboardButton(text="Історія",
                               callback_data='history')
    add_subj_ikb.add(ib1, ib2, ib3, ib4, ib5)
    return add_subj_ikb

def get_regions_ikb():
    ikb = InlineKeyboardMarkup(row_width=1)

    ib1 = InlineKeyboardButton(text="Миколаївська, Сумська, Харківська, Чернігівська області",
                               callback_data='reg_first_group')
    ib2 = InlineKeyboardButton(text="Дніпропетровська, Запорізька, Одеська, Полтавська області",
                               callback_data='reg_second_group')
    ib3 = InlineKeyboardButton(text="Інші області",
                               callback_data='reg_other_group')
    ib4 = InlineKeyboardButton(text="Пропустити",
                               callback_data='skip')
    ikb.add(ib1, ib2, ib3,ib4)
    return ikb
def get_admin_menu_ikb():
    menu_ikb = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text= "Розіслати повідомлення",
                                   callback_data="sending")
    button2 = InlineKeyboardButton(text= "Надай файл зі статистикою",
                                   callback_data="stats")
    button3 = InlineKeyboardButton(text= "Скільки підписників у бота?",
                                   callback_data="users_amount")
    button4 = InlineKeyboardButton(text= "Вийти з адм. панелі",
                                   callback_data="admin_out")
    menu_ikb.add(button1,button2,button3,button4)
    return menu_ikb

def get_admin_sending():
    menu_ikb = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text= "Редагувати",
                                   callback_data="edit_send_message")
    button2 = InlineKeyboardButton(text= "Розіслати",
                                   callback_data="START_SENDING")
    button3 = InlineKeyboardButton(text= "Скасувати",
                                   callback_data="break_sending")
    menu_ikb.add(button1,button2,button3)
    return menu_ikb

from aiogram.dispatcher.filters.state import StatesGroup, State


class Form(StatesGroup):
    math_ent = State()
    ukr_ent = State()
    add_ent = State()
    add_subj_ch = State()
    welcome = State()
    unsub = State()
    feedback = State()
    spec_set = State()
    region_set = State()

    admin = State()
    admin_sending = State()
    admin_sending_1 = State()
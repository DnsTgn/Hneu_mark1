from  aiogram import types

from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext

from ...database.methods.db import database
from ...keyboards import inline
from ...misc import config
from ...misc.forms import Form
from . import calculate_foo
async def feedback(message_or_callback):
    print("[INFO] - Викликана функція feedback")
    text = "Скажи нам як бути краще 🤷‍♂️😉"
    ikb = inline.get_feedback_ikb()
    await Form.feedback.set()
    if isinstance(message_or_callback, types.Message):
        await message_or_callback.bot.send_message(chat_id=message_or_callback.chat.id, text=text,reply_markup=ikb)
    elif isinstance(message_or_callback, types.CallbackQuery):
        await message_or_callback.message.bot.send_message(chat_id=message_or_callback.message.chat.id,
                                                           text=text,reply_markup=ikb)

async def feedback_answer(message_or_callback,state: FSMContext):
    print("[INFO] - Викликана функція feedback_answer")
    await state.reset_state()
    if isinstance(message_or_callback, types.Message):
        text = "Дякуємо за зворотній зв'язок❤️"
        await message_or_callback.bot.forward_message(chat_id=config.admin_chat_id,from_chat_id=message_or_callback.chat.id,message_id=message_or_callback.message_id)
        await message_or_callback.bot.send_message(chat_id=message_or_callback.chat.id, text=text)
    elif isinstance(message_or_callback, types.CallbackQuery):
        if message_or_callback.data == "out":
            await message_or_callback.message.bot.delete_message(chat_id=message_or_callback.message.chat.id,
                                                                 message_id=message_or_callback.message.message_id)
    await menu(message_or_callback)
async def help(message_or_callback):
    print("[INFO] - Викликана функція help")
    text = "🙏🏻 Дякуємо, що користуєтесь нашим ботом, який розроблений факультетом ІТ у <a href =\"www.hneu.edu.ua\">ХНЕУ імені Семена Кузнеця</a>👨‍🎓❤️.\n\n👉 Методика розрахунку конкурсного балу <a href = \"https://telegra.ph/Metodika-rozrahunku-04-18\">тут</a>.\n\n📲Якщо є запитання:\ntelegram: @KhNUE\nkuznets.event@gmail.com"
    if isinstance(message_or_callback,types.Message):
        await message_or_callback.bot.send_message(chat_id=message_or_callback.chat.id, text = text,disable_web_page_preview=True)
    elif isinstance(message_or_callback,types.CallbackQuery):
        await message_or_callback.message.bot.send_message(chat_id=message_or_callback.message.chat.id,
                                                           text=text,disable_web_page_preview=True)
    await menu(message_or_callback)


async def about(message_or_callback):
    print("[INFO] - Викликана функція about")
    text = f"Цей бот \U0001F916 створений у Харківському національному економічному університеті імені Семена Кузнеця \U0001F468\U0001F4BB\U0001F393. \nНаша команда:\n\n▫️Авторі ідеї, куратор проекту та Product Owner – проректор з навчально-методичної роботи та стратегічного розвитку Максим Серпухов \n\n▫️Product Manager – Микита Московкін, студент 1 року навчання за освітнім ступенем «магістр» програми «Міжнародний ІТ менеджмент»\n\n▫️Development Team:\nТовгін Денис – студент 2го курсу факультету ІТ\nЩерба Наталія - студентка 2го курсу факультету ІТ\n\n✅ Дізнавайтеся більше про наші проекти на <a href = \"https://www.hneu.edu.ua\">сайті</a>.  \nМи на зв’язку @KhNUE"

    if isinstance(message_or_callback, types.Message):
        await message_or_callback.bot.send_message(chat_id=message_or_callback.chat.id, text=text,disable_web_page_preview=True)
    elif isinstance(message_or_callback, types.CallbackQuery):
        await message_or_callback.message.bot.send_message(chat_id=message_or_callback.message.chat.id,text=text,disable_web_page_preview=True  )
    await menu(message_or_callback)



    pass
async def welcome_message(message: types.Message):
    print(f"[INFO] - Викликана функція welcome_message, chat_id = {message.chat.id}")
    bot: Bot = message.bot
    DB = database()
    DB.add_id(message.from_user.id)
    await Form.welcome.set()
    text = "😉 Привіт! Я допоможу розрахувати конкурсний бал для вступу😳📊.\nЦе дасть змогу оцінити ☝🏻, на яку спеціальність у вас кращі шанси для вступу! Цей бот розроблено в <a href = \"www.hneu.edu.ua\">Харківському національному економічному університеті імені Семена Кузнеця ❤️👨‍🎓</a>"
    await bot.send_message(chat_id= message.chat.id,text =text,disable_web_page_preview=True)
    await menu(message)

async def menu(message_or_callback):
    print("[INFO] - Викликана функція menu")
    text = "Оберіть команду"
    ikb = inline.get_menu_ikb()
    #await state.reset_state()
    if isinstance(message_or_callback,types.Message):
        await message_or_callback.bot.send_message(chat_id= message_or_callback.chat.id,
                                                text=text,
                                                reply_markup=ikb)
    elif isinstance(message_or_callback,types.CallbackQuery):
        await message_or_callback.bot.send_message(chat_id=message_or_callback.message.chat.id,
                                                   text= text,
                                                   reply_markup=ikb)

def register_user_handlers(dp: Dispatcher):
    # message_handlers------------------------------------------------------
    dp.register_message_handler(welcome_message, commands=['start'])
    dp.register_message_handler(menu, commands=['menu'],state="*")
    dp.register_message_handler(help, commands=['help'], state="*")
    dp.register_message_handler(about, commands= ["about"], state="*")
    dp.register_message_handler(feedback, commands=['feedback'], state="*")
    dp.register_message_handler(feedback_answer,content_types=types.ContentTypes.ANY, state=Form.feedback)
    dp.register_message_handler(calculate_foo.math_question, commands=['calculate'], state="*")
    dp.register_message_handler(calculate_foo.math_answer, state=Form.math_ent)
    dp.register_message_handler(calculate_foo.ukr_answer, state=Form.ukr_ent)
    dp.register_message_handler(calculate_foo.add_subj_mark_answer, state=Form.add_ent)
    dp.register_message_handler(calculate_foo.spec_set_answer, state=Form.spec_set)

    #-----------------------------------------------------------------------

    # call_back_handlers----------------------------------------------------
    dp.register_callback_query_handler(help, lambda call: call.data =="help",state="*")
    dp.register_callback_query_handler(about, lambda call: call.data == "about", state="*")
    dp.register_callback_query_handler(feedback, lambda call: call.data == "feedback", state="*")
    dp.register_callback_query_handler(feedback_answer, lambda call: call.data == "out", state=Form.feedback)
    dp.register_callback_query_handler(calculate_foo.math_question, lambda call: call.data == "calculate", state="*")
    dp.register_callback_query_handler(calculate_foo.add_subj_answer,lambda call: call.data in ['english','physics','chemistry','biology','history'], state=Form.add_subj_ch)
    dp.register_callback_query_handler(calculate_foo.region_answer, lambda call: call.data in ['reg_first_group','reg_second_group',"reg_other_group","skip"], state=Form.region_set)
    # ----------------------------------------------------------------------

    # todo: register all user handlers
    pass


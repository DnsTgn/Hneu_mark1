import asyncio
import logging

from aiogram import exceptions

from aiogram import Dispatcher
from  aiogram import types

from aiogram.dispatcher import FSMContext

from ...database.methods.db import database
from ...handlers.admin.util import stats_file
from ...handlers.user.main import menu
from ...keyboards import inline
from ...misc.config import admin_chat_id as ADMINS
from ...misc.forms import Form


async def admin_menu(message_or_callback):

    if isinstance(message_or_callback,types.Message):
        if message_or_callback.chat.id == ADMINS:
            await Form.admin.set()
            text = "Адмін меню"
            ikb = inline.get_admin_menu_ikb()
            await message_or_callback.bot.send_message(chat_id=message_or_callback.chat.id,text = text,reply_markup=ikb)

    elif isinstance(message_or_callback,types.CallbackQuery):
        if message_or_callback.message.chat.id == ADMINS:
            await Form.admin.set()
            text = "Адмін меню"
            ikb = inline.get_admin_menu_ikb()
            await message_or_callback.bot.send_message(chat_id=message_or_callback.message.chat.id,text = text,reply_markup=ikb)



async def sending_quest(call:types.CallbackQuery,state:FSMContext):

    await call.bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await Form.admin_sending.set()
    text ="Введіть повідомлення для розсилки"
    await call.bot.send_message(chat_id=call.message.chat.id,text = text)




async def sending_answer(message: types.Message):
    if message.from_user.id != message.bot.id:

        await Form.admin_sending_1.set()
        ikb = inline.get_admin_sending()
        state = Dispatcher.get_current().current_state()
        async with state.proxy() as data:
            data['message'] = message
        await message.copy_to(chat_id=message.chat.id)
        await message.bot.send_message(chat_id=message.chat.id,text="Ви впевнені що хочете відправити це повідомлення?",
                                       reply_markup=ikb)

async def sending_answer_1(call: types.CallbackQuery):


    if call.data == "edit_send_message":
        await call.bot.send_message(chat_id=call.message.chat.id,
                                       text="Будь ласка, введіть оновлене повідомлення")
        await Form.admin_sending.set()
    elif call.data == "START_SENDING":
        await sending(call)
    elif call.data == "break_sending":
        await call.bot.send_message(chat_id=call.message.chat.id,text="Розсилку відмінено")
        await admin_menu(call)



async def sending(call:types.CallbackQuery):
    await Form.admin.set()
    await call.bot.send_message(chat_id=call.message.chat.id,
                                text=f"Дочейкайтесь кінця розсилки, вас буде повідомлено")

    try:
        DB = database()
        users = DB.get_all_users()

        # Створюємо повідомлення, яке відправимо підписникам
        state = Dispatcher.get_current().current_state()
        async with state.proxy() as data:
            message = data['message']

        count_bd = len(users)
        count_fact = 0
        count_blocked = 0

        for member in users:
            try:
                await call.bot.send_message(chat_id= int(member),text = message.text)
                count_fact+=1
            except exceptions.BotBlocked:
                count_blocked+=1
            except exceptions.ChatNotFound:
                logging.error(f"chat {member} not found")
            except exceptions.RetryAfter as e:
                logging.info(f"Rate limited by Telegram. Retry after {e.timeout} seconds.")
                await asyncio.sleep(e.timeout)
            except exceptions.TelegramAPIError:
                logging.error(f"Failed to send message to {member}")
        await call.bot.send_message(chat_id=call.message.chat.id,text = f"Всього користувачів в базі даних (за весь час): {count_bd}\nКористувачів які заблокували та видалили бота: {count_blocked}\nВсього розіслано: {count_fact}\n\n<i>Якщо кількість розісланих повідомлень = 0, це може бути пов'язано з неправильним форматом повідомлення розсилки, в повідомленні дозволено писати тільки текст та посилання</i>")
    except exceptions.TelegramAPIError as e:
        logging.error(f"Failed to get chat members. Error: {e}")
    await admin_menu(call)

async def users_amount(call:types.CallbackQuery):
    DB = database()
    text = f"Бот за весь час має <b>{DB.get_users_amount()}</b> користувачів"
    await call.bot.send_message(chat_id=call.message.chat.id,text=text)
    await Form.admin.set()
    await admin_menu(call)

async def stats(call:types.CallbackQuery):
    file_bt = await stats_file()
    file = types.InputFile(path_or_bytesio=file_bt, filename="stat.xlsx")
    await call.bot.send_document(chat_id=call.message.chat.id,document=file)


async def admin_out(call:types.CallbackQuery):
    await call.bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    await menu(call)


def register_admin_handlers(dp: Dispatcher):
    #message -------------------------------------------------
    dp.register_message_handler(admin_menu,commands=['admin','a','adm','administrator'],state="*")
    dp.register_message_handler(sending_answer, content_types=types.ContentTypes.ANY, state= Form.admin_sending)

    #callback ------------------------------------------------
    dp.register_callback_query_handler(sending_quest, lambda call: call.data == "sending",state=Form.admin)
    dp.register_callback_query_handler(users_amount, lambda call: call.data == "users_amount", state=Form.admin)
    dp.register_callback_query_handler(admin_out, lambda call: call.data == "admin_out", state=Form.admin)

    dp.register_callback_query_handler(sending_answer_1, lambda call: call.data in ["edit_send_message","START_SENDING","break_sending"], state=Form.admin_sending_1)
    dp.register_callback_query_handler(stats, lambda call: call.data == "stats", state=Form.admin)

    # todo: register all admin handlers
    pass

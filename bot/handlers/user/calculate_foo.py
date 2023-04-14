from aiogram import types

from AiogramTemplate.bot.database.methods import db_con as db
from AiogramTemplate.bot.keyboards import inline
from AiogramTemplate.bot.misc.forms import Form
from AiogramTemplate.bot.misc import util as valid, config


async def math_question(message_or_callback):
    print("[INFO] - Викликана функція math_question")
    await Form.math_ent.set()
    text = "Введи бал з математики: \nПриклад: 189"

    if isinstance(message_or_callback,types.Message):
        await message_or_callback.bot.send_message(chat_id=message_or_callback.chat.id,text =text)
    if isinstance(message_or_callback,types.CallbackQuery):
        await message_or_callback.bot.send_message(chat_id=message_or_callback.message.chat.id,text=text)

async def math_answer(message:types.Message):
    print("[INFO] - Викликана функція math_answer")
    valid_check = list(valid.nmt_mark_validation(message.text))
    if valid_check[0] == 1:
        db.add_mark('math',int(message.text),message.from_user.id)
        await ukr_question(message)
    elif valid_check[0] == 0:
        text = valid_check[1]
        await message.bot.send_message(chat_id=message.chat.id,text = text)


async def ukr_question(message:types.Message):
    print("[INFO] - Викликана функція urk_question")
    await Form.ukr_ent.set()
    text = "Введи бал з Української мови: \nПриклад: 189"
    await message.bot.send_message(chat_id=message.chat.id, text=text)


async def ukr_answer(message:types.Message):
    print("[INFO] - Викликана функція ukr_answer")
    valid_check = list(valid.nmt_mark_validation(message.text))
    if valid_check[0] == 1:
        db.add_mark('ukr',int(message.text),message.from_user.id)
        await add_subj_quest(message)
    elif valid_check[0] == 0:
        text = valid_check[1]
        await message.bot.send_message(chat_id=message.chat.id,text = text)


async def add_subj_quest(message:types.Message):
    print("[INFO] - Викликана функція add_subj_quest")
    await Form.add_subj_ch.set()
    ikb = inline.get_add_subj_ikb()
    text = "Обери, який дод. предмет ти складав?"
    await message.bot.send_message(chat_id=message.chat.id,text= text,reply_markup=ikb)

async def add_subj_answer(call:types.CallbackQuery):
    print("[INFO] - Викликана функція add_subj_answer")
    db.add_add_subj(call.data,call.from_user.id)
    await add_subj_mark_quest(call)

async def add_subj_mark_quest(call:types.CallbackQuery):
    print("[INFO] - Викликана функція add_subj_mark_answer")
    await Form.add_ent.set()
    text = f"Введи бал з {config.subjects[call.data]} Приклад: 187"
    await call.bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text)

async def add_subj_mark_answer(message:types.Message):
    print("[INFO] - Викликана функція add_subj_mark_answer")
    valid_check = list(valid.nmt_mark_validation(message.text))
    if valid_check[0] == 1:
        db.add_mark('add_subj_mark', int(message.text), message.from_user.id)
        await ukr_question(message)
    elif valid_check[0] == 0:
        text = valid_check[1]
        await message.bot.send_message(chat_id=message.chat.id, text=text)



from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from ...database.methods import db_con as db
from ...handlers.user import main as user_foo
from ...keyboards import inline
from ...misc.forms import Form
from ...misc import util as valid, config, calc


async def math_question(message_or_callback):
    print("[INFO] - Викликана функція math_question")
    await Form.math_ent.set()
    text = "Будь ласка, уведіть цифрою отримані бали на НМТ з математики від 100 до 200 балів, наприклад, <b>189</b>"

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
    text = "Будь ласка, уведіть цифрою отримані бали на НМТ з української мови від 100 до 200 балів, наприклад, <b>175</b>"
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
    text = "Будь ласка, оберіть третій предмет, який ви складали:"
    await message.bot.send_message(chat_id=message.chat.id,text= text,reply_markup=ikb)

async def add_subj_answer(call:types.CallbackQuery):
    print("[INFO] - Викликана функція add_subj_answer")
    db.add_add_subj(call.data,call.from_user.id)
    await add_subj_mark_quest(call)

async def add_subj_mark_quest(call:types.CallbackQuery):
    print("[INFO] - Викликана функція add_subj_mark_answer")
    await Form.add_ent.set()
    text = f"Будь ласка, уведіть цифрою отримані бали на НМТ з {config.subjects[call.data]} від 100 до 200 балів, наприклад, <b>199</b>"
    await call.bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text)

async def add_subj_mark_answer(message:types.Message):
    print("[INFO] - Викликана функція add_subj_mark_answer")
    valid_check = list(valid.nmt_mark_validation(message.text))
    if valid_check[0] == 1:
        db.add_mark('add_subj_mark', int(message.text), message.from_user.id)
        await spec_set_question(message)
    elif valid_check[0] == 0:
        text = valid_check[1]
        await message.bot.send_message(chat_id=message.chat.id, text=text)


async def spec_set_question(message:types.Message):
    print("[INFO] - Викликана функція spec_set_question")
    await Form.spec_set.set()
    text = "Уведіть код спеціальності, для якої потрібно розрахувати конкурсний бал, наприклад: 051\n\nПодивитися всі коди спеціальностей <a href=\"https://telegra.ph/PEREL%D0%86K-galuzej-znan-%D1%96-spec%D1%96alnostej-za-yakimi-zd%D1%96jsnyuyetsya-p%D1%96dgotovka-zdobuvach%D1%96v-vishchoi-osv%D1%96ti-04-18\">тут</a>."
    await message.bot.send_message(chat_id=message.chat.id,text= text,disable_web_page_preview=True)

async def spec_set_answer(message:types.Message):
    print("[INFO] - Викликана функція spec_set_answer")

    state = Dispatcher.get_current().current_state()
    check = valid.spec_validation(message.text)

    if check =="OK":
        async with state.proxy() as data:
            data['spec'] = message.text
            print(f"[INFO] - Для користувача {message.from_user.id} було встановлено спеціальність {data['spec']}")
            db.add_spec_amount(data['spec'])
        await check_spec(message)
    else:
        await message.bot.send_message(chat_id=message.chat.id,text=check)

async def check_spec(message:types.Message):
    print("[INFO] - Викликана функція check_spec")
    state = Dispatcher.get_current().current_state()
    async with state.proxy() as data:
        check = valid.spec_porig_check(data['spec'])
    if check == "NO":
        pass
    else:
        text = f"На цю спеціальність конкурсний бал для вступу на основі повної загальної середньої освіти не може бути менше ніж {check}. Якщо у вас конкурсний бал буде меншим, оберіть іншу спеціальність "
        await message.bot.send_message(chat_id=message.chat.id,text=text)
    await region_question(message)


async def region_question(message:types.Message):
    print("[INFO] - Викликана функція region_question")
    await Form.region_set.set()
    ikb = inline.get_regions_ikb()
    text = "Для додавання регіонального коефіцієнту оберіть область де розташований заклад освіти у який ви плануєте вступити"
    await message.bot.send_message(chat_id=message.chat.id,text=text,reply_markup=ikb)

async def region_answer(call:types.CallbackQuery):
    print("[INFO] - Викликана функція region_answer")
    #['reg_first_group','reg_second_group',"reg_other_group","skip"]

    state = Dispatcher.get_current().current_state()
    async with state.proxy() as data:
        if call.data == 'reg_first_group':
            data['reg_koef'] = 1.07
        elif call.data == 'reg_second_group':
            data['reg_koef'] = 1.04
        elif call.data == 'reg_other_group':
            data['reg_koef'] = 1
        elif call.data == 'skip':
            data['reg_koef'] = 'skiped'
    await call.bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    await calculate(call)

async def calculate(call:types.CallbackQuery):
    print("[INFO] - Викликана функція calcualte")
    result = db.get_all_info(call.from_user.id)
    state = Dispatcher.get_current().current_state()
    reg = 0
    spec = str()
    async with state.proxy() as data:
        spec = data['spec']
        if data['reg_koef'] == 'skiped':
            reg = 1
        else:
            reg = float(data['reg_koef'])
    scores = {'ukr':result[2],'math':result[3],result[1]:result[4]}
    res = await calc.calc_score(reg,spec,scores)
    await print_KB(call,res,state)

async def print_KB(call:types.CallbackQuery,res,state: FSMContext):
    spec = str()
    state1 = Dispatcher.get_current().current_state()
    async with state1.proxy() as data:
        spec = data['spec']
    print("[INFO] - Викликана функція print_KB")
    name = await calc.get_spec_name(spec)
    text = f"На підставі введених даних для спеціальності <i><b>'{spec} {name}'</b></i> з урахуванням:\nГалузевого коефіцієнта ={res[1]}\nРегіонального коефіцієнта ={res[2]}\nВаш конкурсний бал становить: <b>{res[0]}</b>\n\nБудь ласка, перевірте цю інформацію в приймальній комісії, оскільки ми не несемо відповідальності за коректність уведених даних та розрахунку.\n\nДякуємо, що скористалися нашим ботом!\nРозроблено факультетом ІТ у Харківському національному економічному університеті імені Семена Кузнеця"

    #tex = f"Для вибраної спеціальності галузевий коеф ={res[1]}. для вибраного регіону, регіональний коеф ={res[2]}.\nТож ваш бал є:<b>{res[0]}</b>"
    await call.bot.send_message(chat_id=call.message.chat.id,text=text)
    await state.reset_state()
    await user_foo.menu(call)

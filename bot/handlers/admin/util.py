import io

from datetime import datetime


from openpyxl import Workbook
import json
from AiogramTemplate.bot.database.methods import db_con as db
async def stats_file():
    res = db.get_stats()
    datestamp =  datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    amount = 0
    with open(r"D:\HneuMark\AiogramTemplate\bot\koef.json", 'r', encoding="utf-8") as file:
        dictionary = json.load(file)
    for r in res:
        amount += r[1]
        r.insert(1,dictionary[r[0]]['name'])

    amount_users = db.get_users_amount()
    res.insert(0,[])
    res.insert(0,["Загалом розрахунків",amount])
    res.insert(0, ["Кількість користувачів бота", amount_users])
    res.insert(0, ["ДАТА|ЧАС", datestamp])
    workbook = Workbook()
    worksheet = workbook.active
    for r in res:
        worksheet.append(r)

    file_buffer = io.BytesIO()
    workbook.save(file_buffer)
    file_buffer.seek(0)

    # Повертаємо байт-стрічку з файлом xlsx
    return file_buffer


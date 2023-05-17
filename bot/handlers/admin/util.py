import io
import os
import logging
from datetime import datetime
from openpyxl import Workbook
import json
from ...database.methods.db import database


async def stats_file():
    try:
        DB = database()
        res = DB.get_stats()
        datestamp =  datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        amount = 0

        file_path = os.path.join("/app", "AiogramTemplate", "bot", "koef.json")
        with open(file_path, 'r', encoding="utf-8") as file:
            dictionary = json.load(file)
        for r in res:
            amount += r[1]
            r.insert(1,dictionary[r[0]]['name'])

        DB = database()
        amount_users = DB.get_users_amount()
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
        logging.info("stats file`s byte-string was created")
        # Повертаємо байт-стрічку з файлом xlsx
        return file_buffer
    except:
        logging.error("stats file`s byte-string wasn`t created")


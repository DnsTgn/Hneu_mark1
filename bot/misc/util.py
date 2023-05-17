import logging
import os
import json


def nmt_mark_validation(value):
    try:
        mark = int(value)
        if mark < 100 or mark > 200:
            return [0,
                    "📌Неправильний формат вводу, оцінка повинна бути в діапазоні 100-200 (включно), без зайвих символів, наприклад: <b>156</b>"]
    except Exception as ex:
        return [0,"📌Неправильний формат вводу, оцінка повинна бути в діапазоні 100-200 (включно), без зайвих символів, наприклад: <b>156</b>"]
    return [1,"OK"]


def spec_validation(value):
    text = "📌 Будь ласка, перевірте код спеціальності 👉 <a href=\"https://telegra.ph/PEREL%D0%86K-galuzej-znan-%D1%96-spec%D1%96alnostej-za-yakimi-zd%D1%96jsnyuyetsya-p%D1%96dgotovka-zdobuvach%D1%96v-vishchoi-osv%D1%96ti-04-18\">тут</a>.\n ☝🏻Має бути 3 цифри. ✅Наприклад: <b>073</b> або <b>014.02</b>"
    try:
        file_path = os.path.join("/app","AiogramTemplate","bot", "koef.json")
        with open(file_path, 'r') as file:
            dictionary = json.load(file)
        if value not in dictionary:
            return text
    except:
        logging.error("file koef.json wasn`t opened")
        return text

    return "OK"


def spec_porig_check(value):
    try:
        file_path = os.path.join("/app","AiogramTemplate","bot", "porog_spec.json")
        with open(file_path, 'r',encoding='UTF-8') as file:
            dictionary = json.load(file)
        if value in dictionary:
            return dictionary[value]
    except:
         return "NO"
    return "NO"


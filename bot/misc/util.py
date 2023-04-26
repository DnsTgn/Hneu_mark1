import re
import json


def nmt_mark_validation(value):
    try:
        mark = int(value)
        if mark < 100 or mark > 200:
            return [0,
                    "Неправильний формат вводу, оцінка повинна бути в діапазоні 100-200 (включно), без зайвих символів, наприклад: 156"]
    except Exception as ex:
        return [0,"Неправильний формат вводу, оцінка повинна бути в діапазоні 100-200 (включно), без зайвих символів, наприклад: 156"]
    return [1,"OK"]


def spec_validation(value):
    text = "Будь ласка, перевірте код спеціальності <a href=\"https://telegra.ph/PEREL%D0%86K-galuzej-znan-%D1%96-spec%D1%96alnostej-za-yakimi-zd%D1%96jsnyuyetsya-p%D1%96dgotovka-zdobuvach%D1%96v-vishchoi-osv%D1%96ti-04-18|\">тут</a>. Має бути 3 цифри, наприклад: <b>073</b>"
    try:
        with open(r"D:\HneuMark\AiogramTemplate\bot\koef.json", 'r') as file:
            dictionary = json.load(file)
        if value not in dictionary:
            return text
    except:
        return text

    return "OK"


def spec_porig_check(value):
    try:
        with open(r"D:\HneuMark\AiogramTemplate\bot\porog_spec.json", 'r',encoding='UTF-8') as file:
            dictionary = json.load(file)
        if value in dictionary:
            return dictionary[value]
    except:
         return "NO"
    return "NO"


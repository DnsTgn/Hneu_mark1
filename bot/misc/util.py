import re
import json


def nmt_mark_validation(value):
    try:
        mark = int(value)
        if mark < 100 or mark > 200:
            return [0,"Дані введено неправильно, оцінка повинна бути в діапазоні 100-200, включно"]
    except Exception as ex:
        return [0,"Неправильний формат вводу, оцінка повинна бути в діапазоні 100-200(включно),без зайвих символів, наприклад: 156"]
    return [1,"OK"]


def spec_list_validation(value):
    mark_list = None
    try:
        mark_list = re.split("[, ]+", value)
        if len(mark_list) == 0:
            raise ValueError("Пустий список спеціальностей")
        with open(r"D:\HneuMark\AiogramTemplate\bot\koef.json", 'r') as file:
            dictionary = json.load(file)
        for elem in mark_list:
            if elem not in dictionary:
                return f"Некоректо введено спеціальність: {elem}"
    except Exception as ex:
        return "Некоректно введено спеціальність"

    return mark_list
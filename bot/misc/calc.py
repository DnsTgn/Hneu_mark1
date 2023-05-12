import json
import os
import logging


async def get_spec_name(code):
    try:
        file_path = os.path.join("/app","AiogramTemplate","bot", "koef.json")
        with open(file_path, 'r',encoding='UTF-8') as file:
            dictionary = json.load(file)
        name = dictionary[code]['name']
        logging.info("file bot\koef.json was opened")
        return name
    except:
        logging.error(">file bot/koef.json<")
async def get_dict_koef():
    try:
        file_path = os.path.join("/app","AiogramTemplate","bot", "koef.json")
        with open(file_path, 'r') as file:
            dictionary = json.load(file)
        logging.info("file bot\koef.json was opened")
        return dictionary
    except:
        logging.error(">file bot/koef.json<")

async def check_galuz(spec):
    try:
        file_path = os.path.join("/app","AiogramTemplate","bot", "g_koef.json")
        with open(file_path, 'r') as file:
            dictionary = json.load(file)
        if spec in dictionary:
            logging.info(f"galuz for spec{spec} was checked")
            return dictionary[spec]
        else:
            logging.info(f"galuz for spec{spec} was checked")
            return 1
    except:
        logging.error(">file bot/g_koef.json<")
async def calc_score(reg, spec, dict_scores):
    score = 0
    sum_koef = 0

    dictionary_koef = await get_dict_koef()
    galuz = await check_galuz(spec)
    for subj in dict_scores.keys():
        score += dictionary_koef[spec][subj] * dict_scores[subj]
        sum_koef += dictionary_koef[spec][subj]

    try:
        score = (score/sum_koef)*reg * galuz
        logging.debug("score calc is OK")
    except:
        logging.error("division by 0 or type error")

    if score > 200:
        score = 200

    return ["{:.2f}".format(score),galuz,reg]


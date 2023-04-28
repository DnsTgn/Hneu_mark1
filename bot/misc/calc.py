import json


async def get_spec_name(code):
    with open("bot\koef.json", 'r',encoding='UTF-8') as file:
        dictionary = json.load(file)
    name = dictionary[code]['name']
    return name
async def get_dict_koef():
    with open('bot\koef.json', 'r') as file:
        dictionary = json.load(file)
    return dictionary
async def check_galuz(spec):
    with open("bot\g_koef.json", 'r') as file:
        dictionary = json.load(file)
    if spec in dictionary:
        return dictionary[spec]
    else:
        return 1
async def calc_score(reg, spec, dict_scores):
    score = 0
    sum_koef = 0

    dictionary_koef = await get_dict_koef()
    galuz = await check_galuz(spec)
    for subj in dict_scores.keys():
        score += dictionary_koef[spec][subj] * dict_scores[subj]
        sum_koef += dictionary_koef[spec][subj]

    score = (score/sum_koef)*reg * galuz

    if score > 200:
        score = 200

    return ["{:.2f}".format(score),galuz,reg]


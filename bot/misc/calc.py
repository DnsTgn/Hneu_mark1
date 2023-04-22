import json

def get_dict_koef():
    with open(r"D:\HneuMark\AiogramTemplate\bot\koef.json", 'r') as file:
        dictionary = json.load(file)
    return dictionary
def check_galuz(spec):
    with open(r"D:\HneuMark\AiogramTemplate\bot\g_koef.json", 'r') as file:
        dictionary = json.load(file)
    if spec in dictionary:
        return dictionary[spec]
    else:
        return 1
def calc_score(reg, spec, dict_scores):
    score = 0
    sum_koef = 0
    dictionary_koef = get_dict_koef()
    galuz = check_galuz(spec)
    for subj in dict_scores.keys():
        score += dictionary_koef[spec][subj] * dict_scores[subj]
        sum_koef += dictionary_koef[spec][subj]

    score = (score/sum_koef)*reg * galuz

    if score > 200:
        score = 200

    return ["{:.2f}".format(score),galuz,reg]


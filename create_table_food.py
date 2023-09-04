"""
Модуль принимает файл (xls/xlsx) с раскладкой и файл с важностью продуктов (xls/xlsx).
Создает файл (csv): [id; name_of_food; weight; importance] без заголовка

inp_file_name - входной файл с раскладкой (xls/xlsx):
		должен содержать в первом столбце название продукта,
		в последнем - итоговый вес этого продукта
file_with_importance_name - файл с соответствием продуктов и их важности (xls/xlsx):
		должен содержать в первом столбце название продукта,
		во втором - важность (1 - max важность, 4 - min важность),
		первая строка - заголовок
words_for_beg_or_skip - с этих слов начинается подсчет продуктов, либо эти имена скипаются
		(если подсчет уже идет)
out_file_name - имя выходного файла (csv!)

"""

import pandas as pd

inp_file_name = 'in_out_files/раскладка.xlsx'
file_with_importance_name = 'in_out_files/продукты.xlsx'
words_for_beg_or_skip = ['Завтрак', 'Обед', 'Перекус', 'Ужин', 'Прочее']
out_file_name = 'in_out_files/food.csv'


def create_dict_of_prods(xl):
    prods = dict()

    key_of_beg = 0
    for val in xl.values:
        if val[0] in words_for_beg_or_skip:
            key_of_beg = 1
        elif key_of_beg == 1:
            if val[0] not in prods:
                if val[-1] != 0:
                    prods[val[0]] = val[-1]
            else:
                prods[val[0]] += val[-1]

    return prods

def create_csv_prods(prods, imp_dict):
    with open(out_file_name, 'w') as f:
        #line = "id;name;weight;importance\n"
        #f.write(line)
        for i, cur_prod in enumerate(prods):
            name = cur_prod[0]
            weight = int(cur_prod[1])
            importance = imp_dict[name]
            line = "{0};{1};{2};{3}\n".format(
                i + 1,
                name,
                weight,
                importance
            )
            f.write(line)

def find_importance_of_prods():
    xl = pd.read_excel(file_with_importance_name)

    importance = dict()
    for cur in xl.values:
        importance[cur[0]] = cur[1]

    return importance

xl = pd.read_excel(inp_file_name)

prods = create_dict_of_prods(xl)
sort_prods = sorted(list(prods.items()), key = lambda x: x[0][0])

importance = find_importance_of_prods()

create_csv_prods(sort_prods, importance)

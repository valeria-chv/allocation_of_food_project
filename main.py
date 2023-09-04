"""
Модуль предназначен для распределения раскладки между туристами.
Модуль работает с бд tourism (таблицы: food, tourists, tf)
			food: [id, name, weight, importance]
			tourists: [id, name, food_weight]
			tf: [tour_id, food_id]
Создает файл resultfile.xls: [name, food_name, weight]
			
"""

import moduls.database_logic as db
from moduls.selects_logic import *

dbname, user, host, port = "tourism", "postgres", "127.0.0.1", "5432"
password = input("Password: ")

connection = db.create_connection(
    dbname, user, password, host, port
)

connection.autocommit = True
cursor = connection.cursor()

tourists = get_tourists_from_db(cursor)
counts = get_count_of_prods_of_diff_importance(cursor)
add_column_used_in_food(cursor)

while counts[0] + counts[1] != 0:
	for tour in tourists:
		if counts[0] > 0:
			give_prod_to_tour(cursor, importance = 1, tour = tour)
			counts[0] -= 1
		elif counts[1] > 0:
			give_prod_to_tour(cursor, importance = 2, tour = tour)
			counts[1] -= 1
	
	tourists.sort(key = lambda tour: tour.food_weight, reverse = True)

while sum(counts) != 0:
	tour = tourists[0]
	if counts[2] > 0:
		give_prod_to_tour(cursor, importance = 3, tour = tour)
		counts[2] -= 1
	elif counts[3] > 0:
		give_prod_to_tour(cursor, importance = 4, tour = tour)
		counts[3] -= 1
	
	tourists.sort(key = lambda tour: tour.food_weight, reverse = True)

#print(tourists)

write_to_xls_result(cursor)



connection.close()


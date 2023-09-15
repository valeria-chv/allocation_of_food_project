"""
 Модуль создает и заполняет базу данных tourism.
 path_food, path_tourists - путь до файлов с продуктами и туристами соответственно
 food.csv: формат [id; name_of_food; weight; importance] без заголовка
 		   id - id продукта, name_of_food - название,
 		   weight - вес для закупки, importance - важность (1 - max важность, 4 - min важность),
 		   разделитель - ';'
 tourists.csv: формат [id, name, weight] без заголовка
 		   id - id туриста, name - имя,
 		   weight - вес, который должен нести турист (только по продуктам)
 
 """

from moduls.database_logic import *

def create_database(dbname, user, password, host, port):
	
	path_food = 'in_out_files/food.csv'
	path_tourists = 'in_out_files/tourists.csv'
	key = 'add_tables_and_writes' # 'create_and_add_writes'
		
	connection = create_connection(
	    "postgres", user, password, host, port
	)
	connection.autocommit = True
	cursor = connection.cursor()

	if key == 'create_and_add_writes':
		try:
			cursor.execute("CREATE DATABASE tourism")
		finally:
			cursor.close()
			connection.close()


	connection = create_connection(
		dbname, user, password, host, port
	)
	connection.autocommit = True
	cursor = connection.cursor()
	try:
		create_db(cursor, path_food, path_tourists)
	finally:
		cursor.close()
		connection.close()



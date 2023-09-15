from moduls.my_classes import Tourist, Product

def get_tourists_from_db(cursor):
	""" Выгружает всех туристов из бд в список tourists """
	
	cursor.execute("SELECT * FROM tourists")

	tourists = cursor.fetchall()
	tourists = sorted(tourists, key = lambda x: x[2], reverse = True)

	tourists = [Tourist(tour[0], tour[1], tour[2]) for tour in tourists]
	
	return tourists


def get_count_of_prods_of_diff_importance(cursor):
	""" Считает, сколько существует продуктов каждой важности """

	cursor.execute("""
		select count(*)
		from food f
		group by f.importance
		order by f.importance""")
	counts = cursor.fetchall()
	counts = [i[0] for i in counts]
	
	return counts


def add_column_used_in_food(cursor):
	""" Добавляет в таблицу food столбец used """

	cursor.execute("ALTER TABLE food ADD COLUMN used int")


def give_prod_to_tour(cursor, importance, tour, count):
	""" Дает туристу продукт. Т.е. находит в бд подходящий продукт для туриста,
	 добавляет в таблицу tf id туриста и продукта, изменяет оставшийся вес продуктов для туриста,
	 корректирует для продукта столбец used (used = 1)"""

	cursor.execute(f"""
			select *
			from food f
			where f.used is null and f.importance = {importance}
			order by f.weight desc
			limit 1
		""")
	
	product = Product(*cursor.fetchall()[0])
	#print(product)
	
	cursor.execute(f"INSERT INTO tf VALUES ({tour.id}, {product.id}, {count})")
	
	tour.food_weight -= product.weight
	cursor.execute(f"UPDATE food SET used = 1 WHERE id = {product.id}")


def write_to_xls_result(cursor):
	""" Записывает в result.xls распределение продуктов """

	
	query = f"""
		select t.name, food_name, weight
		from tourists t 
		join (
			select *
			from tf t_f
			join (
				select f.id, f.name as food_name, f.weight as weight
				from food f 
			) as f on f.id = t_f.food_id
		) as t_f on t_f.tour_id = t.id
		order by t.id"""

	outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)

	with open('in_files/resultsfile.xls', 'w') as f:
		cursor.copy_expert(outputquery, f)


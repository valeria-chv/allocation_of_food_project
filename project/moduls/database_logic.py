import psycopg2
from psycopg2 import OperationalError

def create_connection(db_name, db_user, db_password, db_host, db_port):
	""" Connect to the PostgreSQL database server """
	
	connection = None
	try:
		connection = psycopg2.connect(
		    database=db_name,
		    user=db_user,
		    password=db_password,
		    host=db_host,
		    port=db_port,
		)
		print("Connection to PostgreSQL DB successful")
	except OperationalError as e:
		print(f"The error '{e}' occurred")
	return connection
    

def create_tables(cursor):
	""" Creates 3 tables: tourists[id, name, food_weight], food[id, name, weight, importance], 
	and tf[tour_id, food_id] """
	
	cursor.execute("""
		
		CREATE TABLE IF NOT EXISTS tourists (
			id int,
			name text,
			food_weight int
		);

		CREATE TABLE IF NOT EXISTS food (
			id int,
			name text,
			weight int,
			importance int
		);

		CREATE TABLE IF NOT EXISTS tf (
			tour_id int,
			food_id int,
			id int
		)
	""")


def add_constraints(cursor):
	""" Add constraints to tables tourists, food, tf """

	cursor.execute("""
		ALTER table tourists
			ADD CONSTRAINT id_t primary key(id),
			ALTER COLUMN name set not null,
			ADD CONSTRAINT food_weight check (food_weight>=0);

		ALTER table food
			ADD CONSTRAINT id_f primary key(id),
			ALTER COLUMN name set not null,
			ADD CONSTRAINT weight check (weight >= 0),
			ADD CONSTRAINT importance check (importance >= 1 and importance <= 4);

		ALTER table tf
			ADD CONSTRAINT tour_id foreign key(tour_id) references tourists(id) ON DELETE CASCADE,
			ADD CONSTRAINT food_id foreign key(food_id) references food(id) ON DELETE CASCADE;

	""")


def copy_data_to_db(cursor, path_food, path_tourists):
	""" Copy data from csv to db.
	Tables: food[id, name, weight, importance], tourists[id, name, food_weight] """
	
	with open(path_food, 'r') as f:
		cursor.copy_from(f, 'food', columns=('id', 'name', 'weight', 'importance'), sep=";")

	with open(path_tourists, 'r') as f:
		cursor.copy_from(f, 'tourists', columns=('id', 'name', 'food_weight'), sep=",")


def create_db(cursor, path_food, path_tourists):
	""" Creates db (create tables; add constrains, copy data from csv to db if it is empty) """

	create_tables(cursor)
	
	cursor.execute("SELECT count(*) FROM food")
	count_in_food = cursor.fetchall()
	cursor.execute("SELECT count(*) FROM tourists")
	count_in_tour = cursor.fetchall()
	#print(count_in_food, '!', count_in_tour)
	if count_in_food[0][0] == count_in_tour[0][0] == 0:
		#print(1)
		add_constraints(cursor)
		#copy_data_to_db(cursor, path_food, path_tourists)



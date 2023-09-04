class Tourist:
	def __init__(self, id, name, food_weight):
		self.id = id
		self.name = name
		self.food_weight = food_weight
		
	def __repr__(self):
		return (f"[id = {self.id}, name = {self.name}, weight = {self.food_weight}]")
		
	def __str__(self):
		return self.__repr__()
		

class Product:
	def __init__(self, id, name, weight, importance, *args):
		self.id = id
		self.name = name
		self.weight = weight
		self.importance = importance
		
	def __repr__(self):
		return (f"[id = {self.id}, name = {self.name}, weight = {self.weight}, importance = {self.importance}]")
		
	def __str__(self):
		return self.__repr__()

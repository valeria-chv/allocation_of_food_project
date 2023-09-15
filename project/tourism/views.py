from django.views.generic import ListView, DetailView
from .models import Tourists, Food, Tf
from django.shortcuts import render, redirect
from django.http import HttpResponse

class HomePageView(ListView):
	model = Tourists
	template_name = 'home.html'

class TouristListView(ListView):
	model = Tourists
	template_name = 'tourist_list.html'
	
class FoodListView(ListView):
	model = Food
	template_name = 'food_list.html'
	
class TourAllView(ListView):
	model = Tf
	template_name = 'tf_list.html'
	extra_context = {"count":Tourists.objects.count}
	
class TourDetailView(DetailView):
	model = Tourists
	template_name = 'tf_one.html'
	context_object_name = 'object'
	pk_url_kwarg = 'id'
	extra_context = {"tf":Tf.objects.all()}

from django.conf import settings
dbname, user, password, host, port = settings.DATABASES['default']['NAME'], settings.DATABASES['default']['USER'], settings.DATABASES['default']['PASSWORD'], settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT']


def create_csv(request):
	
	try: 
		from moduls.create_table_food import create_table_food
		create_table_food()
		return redirect('home')
		
	except:
		return HttpResponse('Error!')
	

def create_db(request):
	
	try:
		from moduls.create_database import create_database
		create_database(dbname, user, password, host, port)
		
		import csv
		
		file='in_files/tourists.csv'
		tourists = []
		with open(file, newline='') as File: 
			reader = csv.reader(File)
			for row in reader:
				t = Tourists(id = row[0], name = row[1], food_weight = row[2])
				tourists.append(t)
		
		Tourists.objects.bulk_create(tourists)
		
		
		file='in_files/food.csv'
		foods = []
		with open(file, newline='') as File: 
			reader = csv.reader(File, delimiter=';')
			for row in reader:
				t = Food(id = row[0], name = row[1], weight = row[2], importance = row[3])
				foods.append(t)
		
		
		Food.objects.bulk_create(foods)
		
		return redirect('home')
		
	except:
		return HttpResponse('Error!')


def process_data(request):
	
	try:
		from moduls.main import main
		main(dbname, user, password, host, port)
		
		return redirect('home')
	
	except:
		return HttpResponse('Error!')
	
	

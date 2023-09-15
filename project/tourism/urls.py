from django.urls import path
from . import views

urlpatterns = [
	path('', views.HomePageView.as_view(), name = 'home'),
    path('tourists/', views.TouristListView.as_view(), name = 'tourists'),
    path('food/', views.FoodListView.as_view(), name = 'food'),
    path('tf/', views.TourAllView.as_view(), name = 'tf_all'),
    path('tf/<int:id>/', views.TourDetailView.as_view(), name = 'tf_detail'),
    path('create_csv/', views.create_csv, name = 'create_csv'),
    path('create_db/', views.create_db, name = 'create_db'),
    path('process_data/', views.process_data, name = 'process_data'),
]

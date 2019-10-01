from assets_app import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('assets/', views.assets, name='assets'),
    path('categories/', views.categories, name='categories'),
    path('locations/', views.locations, name='locations'),  
]
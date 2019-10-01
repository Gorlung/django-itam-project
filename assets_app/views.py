from django.shortcuts import render
from assets_app.models import Category, Location

# Create your views here.

def index(request):
    return render(request, 'assets_app/index.html', context=None)

def assets(request):
    return render(request, 'assets_app/assets.html', context=None)

def categories(request):
    return render(request, 'assets_app/categories.html', {'categories': Category.objects.all()})

def locations(request):
    return render(request, 'assets_app/locations.html', {'locations': Location.objects.all()})

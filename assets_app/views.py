from django.shortcuts import render
from assets_app.models import Category, Location, Asset
from assets_app.forms import AssetForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Create your views here.

def index(request):
    return render(request, 'assets_app/index.html', context=None)

def assets(request):
    return render(request, 'assets_app/assets.html', context=None)

def categories(request):
    return render(request, 'assets_app/categories.html', {'categories': Category.objects.all()})

def locations(request):
    return render(request, 'assets_app/locations.html', {'locations': Location.objects.all()})

class AssetsListView(ListView):
    model = Asset
    paginate_by = 3
    def get_queryset(self):
        return Asset.objects.all().order_by('-added_on')

class AssetDetailView(DetailView):
    model = Asset

class CreateAssetView(CreateView,LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'assets_app/asset_detail.html'
    form_class = AssetForm
    model = Asset

class AssetUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'assets_app/asset_detail.html'
    form_class = AssetForm
    model = Asset

class AssetDeleteView(LoginRequiredMixin,DeleteView):
    model = Asset
    success_url = reverse_lazy('assets_list')

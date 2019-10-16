from django.shortcuts import render
from assets_app.models import Category, Location, Asset, Change
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
    def get_context_data(self, **kwargs):
        context = super(AssetDetailView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        context['change'] = Change.objects.filter(asset=pk) #whatever you would like
        return context

class CreateAssetView(CreateView,LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'assets_app/asset_detail.html'
    form_class = AssetForm
    model = Asset

class AssetUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'assets_app/asset_detail.html'
    form_class = AssetForm
    model = Asset
    def form_valid(self, form):
        asset_item = form.save(commit=False)
        change_item = Change(asset=asset_item, change_details='something has changed 3', author=self.request.user)
        change_item.save()
        asset_item.save()
        return super(AssetUpdateView, self).form_valid(form)



class AssetDeleteView(LoginRequiredMixin,DeleteView):
    model = Asset
    success_url = reverse_lazy('assets_list')

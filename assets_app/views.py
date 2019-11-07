from django.shortcuts import render
from assets_app.models import Category, Location, Asset, Change, Employee
from assets_app.forms import AssetForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect



def index(request):
    return redirect('/assets/')

def logout_view(request):
    logout(request)
    return render(request, 'assets_app/index.html', context=None)


class SameLocationOnlyMixin(object):
    def has_permissions(self,**kwargs):
        user_locations = Employee.objects.filter(user=self.request.user.id).values_list('permitted_locations',flat=True)
        asset_locations = Asset.objects.get(pk=self.kwargs.get('pk',0)).location.id
        return asset_locations in user_locations
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            return render(request, 'assets_app/no_access.html', context=None)
        return super(SameLocationOnlyMixin, self).dispatch(request, *args, **kwargs)

class AssetsListView(LoginRequiredMixin,ListView):
    model = Asset
    paginate_by = 20
    def get_queryset(self):
        order = self.request.GET.get('orderby','inventory_number')
        return Asset.objects.filter(location__id__in=Employee.objects.filter(user=self.request.user.id).values('permitted_locations')).order_by(order)
    def get_context_data(self, **kwargs):
        context = super(AssetsListView, self).get_context_data(**kwargs)
        context['orderby'] = self.request.GET.get('orderby','inventory_number')
        return context

class AssetDetailView(LoginRequiredMixin,SameLocationOnlyMixin, DetailView):
    model = Asset
    def get_context_data(self, **kwargs):
            context = super(AssetDetailView, self).get_context_data(**kwargs)
            pk = self.kwargs.get('pk', 0)
            context['change'] = Change.objects.filter(asset=pk)
            return context


class CreateAssetView(LoginRequiredMixin,CreateView):
    form_class = AssetForm
    model = Asset
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(CreateAssetView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user_id'] = self.request.user.id
        return kwargs
    def form_valid(self, form):
        form.instance.category_id = self.request.POST['category']
        return super(CreateAssetView, self).form_valid(form)

class AssetUpdateView(LoginRequiredMixin,SameLocationOnlyMixin,UpdateView):
    form_class = AssetForm
    model = Asset
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AssetUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user_id'] = self.request.user.pk
        return kwargs
    def get_context_data(self, **kwargs):
            context = super(AssetUpdateView, self).get_context_data(**kwargs)
            asset = Asset.objects.get(id=self.kwargs.get('pk', 0))
            context['initial_category'] = Category.objects.get(id=asset.category.pk)
            return context
    def form_valid(self, form, **kwargs):
        asset_item = form.save(commit=False)
        changes = form.changed_data
        asset = Asset.objects.get(id=self.kwargs.get('pk', 0))
        initial_category = Category.objects.get(id=asset.category.pk)
        changed_category = Category.objects.get(id=self.request.POST['category'])
        if changes or initial_category.id != changed_category.id:
            form.instance.category_id = self.request.POST['category']
            changes_dict = ''
            for k in changes:
                changes_dict += ' '+ k +' to ' + str(form.cleaned_data.get(k)) + ';'
            if initial_category.id != changed_category.id:
                changes_dict += ' ' + str(initial_category.name) + ' to ' + str(changed_category.name) + ';'  
            change_item = Change(asset=asset_item, change_details=changes_dict, author=self.request.user)
            change_item.save()
            asset_item.save()
        return super(AssetUpdateView, self).form_valid(form)



class AssetDeleteView(LoginRequiredMixin,DeleteView):
    model = Asset
    success_url = reverse_lazy('assets_list')

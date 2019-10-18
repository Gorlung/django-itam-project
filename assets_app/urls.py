from assets_app import views
from django.urls import path
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    path('assets/', views.AssetsListView.as_view(), name='assets_list'),
    url(r'^assets/(?P<pk>\d+)$', views.AssetDetailView.as_view(), name='asset_detail'),
    url(r'^assets/(?P<pk>\d+)/edit/$', views.AssetUpdateView.as_view(), name='asset_edit'),
    url(r'^assets/(?P<pk>\d+)/delete/$', views.AssetDeleteView.as_view(), name='asset_delete'),
    path('assets/new/', views.CreateAssetView.as_view(), name='asset_new'),
]
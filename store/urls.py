from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_all, name='product_all'),
    path('<slug:slug>', views.product_detail, name='product_detail'),
    path('search/', views.search_products, name='search_products'),
    path('shop/<slug:category_slug>/', views.category_list, name='category_list'),
]

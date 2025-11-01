from django.urls import path
from . import views

app_name = 'app_home'

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:category_id>/', views.filter_products_by_category, name='filter_products_by_category'),
    path('productbyname/', views.filter_products_by_name, name='filter_products_by_name'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]
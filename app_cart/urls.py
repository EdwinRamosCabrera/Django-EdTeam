
from django.urls import path
from app_cart import views

app_name = 'app_cart'  

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('add_product_cart/<int:product_id>/', views.add_product_cart, name='add_product_cart'),
    path('delete_product_cart/<int:product_id>/', views.delete_product_cart, name='delete_product_cart'),
    path('clean_cart/', views.clean_cart, name='clean_cart'),
]
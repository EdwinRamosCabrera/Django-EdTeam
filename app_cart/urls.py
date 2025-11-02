
from django.urls import path
from app_cart import views

app_name = 'app_cart'  

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('cart/add_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/clean/', views.clean_cart, name='clean_cart'),
    path('cart/register/', views.register_order, name='register_order'),
]
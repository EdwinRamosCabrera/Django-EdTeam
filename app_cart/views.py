from django.shortcuts import render
from app_products.models import Product
from . models import Cart

"""View function for shopping cart"""
def cart(request):
    return render(request, '../templates/carrito.html')

def add_to_cart(request, product_id):
    cantidad = 1
    object_product = Product.objects.get(id=product_id)
    cart_product = Cart(request) # Cart receives a request object when it initializes
    cart_product.add(object_product, cantidad)
    print(request)
    print(request.session['cart'])

    return render(request, '../templates/carrito.html')

def clean_cart(request):
    pass

def register_order(request):
    pass
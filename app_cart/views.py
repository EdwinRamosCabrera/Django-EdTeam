from django.shortcuts import render
from app_products.models import Product
from . models import Cart

"""View function for shopping cart"""
def cart(request):
    return render(request, '../templates/carrito.html')

def add_to_cart(request, product_id):
    if request.method == 'POST':
        # request.POST is a QueryDict (mapping), not callable. Use get() or []
        # Use get with a default and guard against invalid integers.
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (TypeError, ValueError):
            quantity = 1
    else:
        # If not a POST request, default quantity is 1
        quantity = 1
        
    object_product = Product.objects.get(id=product_id)
    cart_product = Cart(request) # Cart receives a request object when it initializes
    cart_product.add(object_product, quantity)
    # print(request)
    # print(request.session['cart'])

    return render(request, '../templates/carrito.html')

def delete_product_cart(request, product_id):
    object_product = Product.objects.get(id=product_id)
    cart_product = Cart(request)
    cart_product.delete(object_product)
    return render(request, '../templates/carrito.html')

def clean_cart(request):
    cart_product = Cart(request)
    cart_product.clean()
    return render(request, '../templates/carrito.html')

def register_order(request):
    pass
from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from app_products.models import Category, Product

"""View function for the product catalog"""
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, '../templates/index.html', context)

"""View function for filter products by category"""
def filter_products_by_category(request, category_id):
    products = Product.objects.filter(category_id=category_id)
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, '../templates/index.html', context)


"""View function to filter products by name"""
def filter_products_by_name(request):
    # use get to avoid KeyError if 'name' not present and strip whitespace
    query = request.POST.get('name', '').strip()

    # Use case-insensitive contains lookup so searches are not sensitive to
    # uppercase/lowercase differences (e.g. 'camisa' == 'Camisa' == 'CAMISA').
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        # If no query provided, show all products (change behavior if you prefer none)
        products = Product.objects.all()
        categories = Category.objects.all()
        context = {
            'products': products,
            'categories': categories
        }
    return render(request, '../templates/index.html', context)

"""View function for product detail"""
def product_detail(request, product_id):
    # product = Product.objects.get(id=product_id)
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    context = {
        'product': product,
        'categories': categories
    }
    return render(request, '../templates/producto.html', context)


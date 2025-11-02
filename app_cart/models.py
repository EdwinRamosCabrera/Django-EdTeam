from django.db import models

class Cart:

    def __init__(self, request):
        self.request = request 
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity):
        self.cart[str(product.id)] = {
            'product_id': product.id,
            'name': product.name,
            'quantity': quantity,
            'price': str(product.price),
            'image': product.image.url,
            'category': product.category.name,
            'subtotal': str(float(product.price) * quantity)
        }
        self.save()

    """ Save changes to shopping cart """
    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def remove(self, product):
        if str(product.id) in self.cart:
            del self.cart[str(product.id)]
            self.save()

    def get_total_price(self):
        return sum(item['quantity'] * float(item['price']) for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.save()
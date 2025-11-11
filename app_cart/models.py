from decimal import Decimal
from django.db import models

class Cart:

    def __init__(self, request):
        self.request = request 
        self.session = request.session
        cart = self.session.get('cart')
        total_amount = self.session.get('total_amount')
        if not cart:
            cart = self.session['cart'] = {}
            total_amount = self.session['total_amount'] = "0.00"
        self.cart = cart
        self.total_amount = float(total_amount)

    def add(self, product, quantity):
        if str(product.id) not in self.cart.keys():
            self.cart[str(product.id)] = {
                'product_id': product.id,
                'name': product.name,
                'quantity': quantity,
                'price': str(product.price),
                'image': product.image.url,
                'category': product.category.name,
                # compute as Decimal, quantize, then convert to string for storage
                'subtotal': str((Decimal(str(product.price)) * Decimal(str(quantity))).quantize(Decimal('0.01')))
            }
        else:
            # Update quantity and subtotal
            self.cart[str(product.id)]['quantity'] += quantity
            # price and quantity stored as strings/numbers — convert to Decimal safely using str()
            new_subtotal = (Decimal(str(self.cart[str(product.id)]['price'])) * Decimal(str(self.cart[str(product.id)]['quantity']))).quantize(Decimal('0.01'))
            self.cart[str(product.id)]['subtotal'] = str(new_subtotal)
        
        self.save()

    """ Save changes to shopping cart """
    def save(self):
        total_amount = sum(Decimal(item['subtotal']) for item in self.cart.values())
        self.session['cart'] = self.cart
        self.session['total_amount'] = str(Decimal(total_amount).quantize(Decimal('0.01')))
        self.session.modified = True

    def delete(self, product):
        if str(product.id) in self.cart:
            del self.cart[str(product.id)]
            self.save()

    def clean(self):
        del self.session['cart']
        self.session['total_amount'] = "0.00"
        self.session.modified = True
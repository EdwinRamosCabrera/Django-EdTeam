from django.db import models
from django.contrib.auth.models import User
from app_products.models import Product

# Create your models here.
class Client(models.Model):
    dni = models.CharField(max_length=8)
    gender = models.CharField(max_length=1, default='M')
    phone = models.CharField(max_length=15)
    birth_date = models.DateField(null=True)
    address = models.TextField()
    user = models.OneToOneField(User, on_delete=models.RESTRICT)

    def __str__(self):
        return f"{self.dni}"
    

class Order(models.Model):
    STATUS_CHOICES = (
        ('0', 'Pending'),
        ('1', 'Processing'),
        ('2', 'Shipped'),
        ('3', 'Delivered'),
        ('4', 'Cancelled'),
    )
    client = models.ForeignKey(Client, on_delete=models.RESTRICT)
    registration_date = models.DateTimeField(auto_now_add=True)
    number_order = models.CharField(max_length=20, unique=True)
    amount_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=1, default='0', choices=STATUS_CHOICES)

    def __str__(self):
        return f"Order {self.number_order} - {self.client.dni}"
    
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.RESTRICT)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detail for Order {self.order.number_order} - {self.product_name}"
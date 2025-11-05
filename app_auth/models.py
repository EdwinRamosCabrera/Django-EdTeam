from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    dni = models.CharField(max_length=8, unique=True)
    gender = models.CharField(max_length=1, default='M')
    phone = models.CharField(max_length=15)
    birth_date = models.DateField(null=True, blank=True)
    address = models.TextField()
    user = models.OneToOneField(User, on_delete=models.RESTRICT)

    def __str__(self):
        return f"{self.dni}"
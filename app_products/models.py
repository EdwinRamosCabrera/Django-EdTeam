from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nombre')
    code = models.CharField(max_length=50, unique=True, verbose_name='Código')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Slug')
    category = models.ForeignKey('Category', on_delete=models.RESTRICT, verbose_name='Categoría')
    description = models.TextField(null=True, blank=True, verbose_name='Descripción')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    stock = models.IntegerField(verbose_name='Stock')
    image = models.ImageField(upload_to='images/products/', blank=True, null=True, verbose_name='Imagen')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    code = models.CharField(max_length=50, unique=True, verbose_name='Código')
    description = models.TextField(blank=True, null=True, verbose_name='Descripción')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
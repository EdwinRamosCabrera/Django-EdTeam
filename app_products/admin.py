from django.contrib import admin
from app_products.models import Product, Category

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'price', 'stock', 'created', 'updated')
    list_editable = ('price', 'stock')
    search_fields = ('name', 'code', 'category__name')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

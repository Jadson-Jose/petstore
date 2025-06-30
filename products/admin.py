from django.contrib import admin
from .models import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'name', 
        'stock',
        'category',
        'is_active',
        'created_at',
    )
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'name', 
        'created_at'
    )
    search_fields = ('name',)
    ordering = ('name',)


from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "stock",
        "category",
        "active",
        "created_at"
    )
    list_filter = (
        "category",
        "active",
        "created_at",
    )
    search_fields = (
        "name",
        "description",
    )
    ordering = ("-created_at",)
    autocomplete_fields = ("category",)

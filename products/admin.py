from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'name', 
        'formatted_price',
        'stock_status',
        'stock',
        'category_link',
        'is_active',
        'is_active_icon',
        'created_at',
    )
    list_filter = (
        'category',
        'is_active',
        'created_at',
        'updated_at',
    )
    list_editable = (
        'stock',
        'is_active'
    )
    search_fields = (
        'name',
        'description',
        'sku',  # Se existir
    )
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'description', 'category')
        }),
        ('Estoque e Preço', {
            'fields': ('stock', 'price'),
        }),
        ('Status', {
            'fields': ('is_active',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def formatted_price(self, obj):
        if hasattr(obj, 'price'):
            return f"R$ {obj.price:,.2f}"
        return "-"
    formatted_price.short_description = "Preço"
    
    def stock_status(self, obj):
        if obj.stock <= 0:
            color = 'red'
            status = 'Sem estoque'
        elif obj.stock <= 10:
            color = 'orange'
            status = f'Baixo ({obj.stock})'
        else:
            color = 'green'
            status = f'OK ({obj.stock})'
        
        return format_html(
            '<span style="color: {};">{}</span>',
            color, status
        )
    stock_status.short_description = "Estoque"
    
    def category_link(self, obj):
        if obj.category:
            url = reverse('admin:products_category_change', args=[obj.category.pk])
            return format_html('<a href="{}">{}</a>', url, obj.category.name)
        return "-"
    category_link.short_description = "Categoria"
    
    def is_active_icon(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">✓ Ativo</span>')
        return format_html('<span style="color: red;">✗ Inativo</span>')
    is_active_icon.short_description = "Status"
    
    def ativar_produtos(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(
            request, 
            f'{updated} produto(s) ativado(s) com sucesso.'
        )
    ativar_produtos.short_description = "Ativar produtos selecionados"
    
    def desativar_produtos(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(
            request, 
            f'{updated} produto(s) desativado(s) com sucesso.'
        )
    desativar_produtos.short_description = "Desativar produtos selecionados"
    
    actions = ['ativar_produtos', 'desativar_produtos']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'name', 
        'product_count',
        'created_at'
    )
    search_fields = ('name', 'description')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    
    def product_count(self, obj):
        count = obj.products.count() 
        return f"{count} produto(s)"
    product_count.short_description = "Qtd. Produtos"
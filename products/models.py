from django.db import models

class Category(models.Model):
    name = models.CharField("Nome", max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField("Nome", max_length=255)
    description = models.TextField("Descrição")
    price = models.DecimalField("Preço", max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField("Estoque")
    category = models.ForeignKey(Category,
                                 verbose_name="Categoria",
                                 on_delete=models.CASCADE, 
                                 related_name='products'
                                )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['-created_at']
        
        def __str__(self):
            return self.name

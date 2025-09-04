from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class ProductStatus(models.TextChoices):
    PENDENTE = 'pendente', 'Pendente'
    APROVADO = 'aprovado', 'Aprovado'
    REJEITADO = 'rejeitado', 'Rejeitado'

class Category(models.Model):
    name = models.CharField("Nome", max_length=255, unique=True)
    slug = models.SlugField(
        "Slug",
        max_length=255,
        unique=True,
        blank=True,
        editable=False,
        help_text="Preenchido automaticamente a partir do nome"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["name"]
        
    def __str__(self):
        return self.name
     
    def save(self, *args, **kwargs):
        if not self.slug:
            # Remove acentos e caracteres esepeciais, gerar slug limpo
            self.slug = slugify(self.name, allow_unicode=False)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})
    
    
class Product(models.Model):
    name = models.CharField("Nome", max_length=255, blank=False, unique=True)
    description = models.TextField("Descrição")
    price = models.DecimalField("Preço", max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField("Estoque")
    image = models.ImageField(upload_to='products/images/', blank=True, null=True)
    category = models.ForeignKey(
        Category,
        verbose_name="Categoria",
        on_delete=models.CASCADE, 
        related_name="products"
    )
    status = models.CharField(
        max_length=20,
        choices=ProductStatus.choices,
        default=ProductStatus.PENDENTE
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

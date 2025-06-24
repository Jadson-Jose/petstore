from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Categoria")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Nome",
        help_text="Nome do produto"
    )
    description = models.TextField(
        verbose_name="Descrição",
        help_text="Descrição detalhada do produto"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Preço",
        help_text="Preço unitário do produto"
    )
    stock = models.PositiveIntegerField(
        verbose_name="Estoque",
        help_text="Quantidade disponível em estoque"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Categoria"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última atualização"
    )
    active = models.BooleanField(
        default=True,
        verbose_name="Ativo",
        help_text="Indica se um produto está visível e disponível para venda"
    )

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - R$ {self.price:.2f}"

from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Categoria")
    # Adicionando campos necessários para a home
    featured = models.BooleanField(
        default=False,
        verbose_name="Em destaque",
        help_text="Marque para exibir esta categoria na página inicial"
    )
    description = models.TextField(
        verbose_name="Descrição",
        help_text="Descrição para exibição na home",
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to='categories/',
        verbose_name="Imagem",
        help_text="Imagem para exibição na home",
        blank=True,
        null=True
    )
    icon_class = models.CharField(
        max_length=50,
        default="fas fa-paw",
        verbose_name="Classe do Ícone",
        help_text="Classe FontAwesome para o ícone (ex: fas fa-dog)"
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        verbose_name="Slug",
        help_text="Identificador único para URLs"
    )

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


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
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="Desconto (%)",
        help_text="Percentual de desconto a ser aplicado"
    )
    sold = models.PositiveIntegerField(
        default=0,
        verbose_name="Unidades Vendidas",
        help_text="Quantidade de unidades vendidas deste produto"
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
    image = models.ImageField(
        upload_to='products/',
        verbose_name="Imagem Principal",
        help_text="Imagem principal do produto",
        blank=True,
        null=True
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        verbose_name="Slug",
        help_text="Identificador único para URLs"
    )

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - R$ {self.price:.2f}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def discounted_price(self):
        """Calcula o preço com desconto"""
        return self.price * (1 - self.discount / 100)

    @property
    def is_new(self):
        """Verifica se o produto é novo (criado nos últimos 30 dias)"""
        from django.utils import timezone
        return (timezone.now() - self.created_at).days <= 30

from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Nome",
        help_text="Nome da categoria (ex: Eletrônicos, Roupas)"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="Slug",
        help_text="Texto amigável para URLs, ex: eletrônicos"
    )
    feature = models.BooleanField(
        default=False,
        verbose_name="Em destaque"
    )
    description = models.TextField(
        verbose_name="Descrição",
        help_text="Breve descrição par exibição na home",
        blank=True
    )
    image = models.ImageField(
        upload_to="categories/",
        verbose_name="Imagem",
        help_text="Imagem para exibição na home",
        blank=True,
        null=True
    )
    icon_class = models.CharField(
        max_length=50,
        verbose_name="Classe de Ícone",
        help_text="Classe FontAwesome para o ícone (ex: fas fa-dog)",
        default="fas fas-paw"
    )

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

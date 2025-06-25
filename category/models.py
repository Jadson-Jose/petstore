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

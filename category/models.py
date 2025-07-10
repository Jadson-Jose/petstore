from django.test import TestCase
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Nome da Categoria",
        help_text="Nome da categoria (ex: Rações, Roupas)"
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        verbose_name="Slug",
        help_text="Versão amigável para URLs (gerado automaticamente)"
    )
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """
        Gera automaticamente o slug baseado no nome se não for fornecido
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('category_detail', kwargs={'slug': self.slug})

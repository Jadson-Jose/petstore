from django.test import TestCase
from .models import Category
from django.db import IntegrityError
from django.utils.text import slugify


class CategoryModelTest(TestCase):
    def test_create_category_with_slug_generate(self):
        cat = Category.objects.create(name="Roupas")
        self.assertEqual(cat.slug, "roupas")

    def test_slug_manual_respect(self):
        cat = Category.objects.create(name="Tênis", slug="tenis-top")
        self.assertEqual(cat.slug, "tenis-top")

    def test_slugify_with_specials_characters(self):
        name = "Elerônicos & Acessórios"
        cat = Category.objects.create(name=name)
        self.assertEqual(cat.slug, slugify(name))

    def test_slug_must_be_unique(self):
        Category.objects.create(name="Som", slug="som-unico")
        with self.assertRaises(IntegrityError):
            Category.objects.create(name="Outro Som", slug="som-unico")

    def test_str_representation(self):
        cat = Category.objects.create(name="Games")
        self.assertEqual(str(cat), "Games")

    def test_alphabetical_sorting(self):
        c1 = Category.objects.create(name="Higiene")
        c2 = Category.objects.create(name="Pessoal")
        categories = list(Category.objects.all())
        # self.assertEqual(categories, [c2, c1])
        self.assertEqual(categories, [c1, c2])

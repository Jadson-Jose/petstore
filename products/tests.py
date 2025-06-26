from django.test import TestCase
from products.models import Category, Product
from django.utils import timezone


class CategotyModelTest(TestCase):
    def test_create_category(self):
        category = Category.objects.create(name="Brinquedos")
        self.assertEqual(category.name, "Brinquedos")
        self.assertEqual(str(category), "Brinquedos")


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Alimentos")

    def test_create_product(self):
        product = Product.objects.create(
            name="Ração Premium",
            description="Ração para cães adultos de grande porte.",
            price=199.90,
            stock=20,
            category=self.category
        )
        self.assertEqual(product.name, "Ração Premium")
        self.assertEqual(product.stock, 20)
        self.assertEqual(product.active, True)
        self.assertEqual(product.category.name, "Alimentos")
        self.assertTrue(product.created_at <= timezone.now())
        self.assertTrue(product.updated_at <= timezone.now())

    def test_repr_product(self):
        product = Product.objects.create(
            name="Coleira LED",
            description="Coleira com luz de segurança para passeios noturnos.",
            price=59.90,
            stock=15,
            category=self.category
        )
        self.assertIn("Coleira LED", str(product))
        self.assertIn('R$', str(product))


class ProductQuerysetTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="Acessórios")

        Product.objects.create(
            name="Coleira Neon",
            description="Coleira refletiva para passeios noturnos",
            price=29.90,
            stock=10,
            active=True,
            category=self.cat
        )

        Product.objects.create(
            name="Brinquedo Mordedor",
            description="Brinquedo de borracha resistente",
            price=19.90,
            stock=0,
            active=False,
            category=self.cat
        )

    def test_product_active_querset(self):
        active = Product.objects.filter(active=True)
        self.assertEqual(active.count(), 1)
        self.assertEqual(active.first().name, "Coleira Neon")

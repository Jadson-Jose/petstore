from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import Category, Product
from django.db import IntegrityError, transaction

class CategoryModelTest(TestCase):
    def setUp(self):
        """Configurar dados para os testes"""
        self.category = Category.objects.create(name="Rações para cães")
        
    def test_category_creation(self):
        self.assertEqual(self.category.name, "Rações para cães")
        self.assertTrue(self.category.created_at)
        self.assertTrue(self.category.updated_at)
        
    def test_category_str_method(self):
        self.assertEqual(str(self.category), "Rações para cães")
        
    def test_category_verbose_names(self):
        self.assertEqual(Category._meta.verbose_name, "Categoria")
        self.assertEqual(Category._meta.verbose_name_plural, "Categorias")
        
    def test_category_name_max_length(self):
        max_length = Product._meta.get_field('name').max_length
        long_name = "x" * (max_length + 1)
      
        category = Category(name=long_name)
        with self.assertRaises(ValidationError):
            category.full_clean()
            
    def test_category_name_unique(self):
        """Testa se o nome da categoria é único"""
        with self.assertRaises(IntegrityError):
            Category.objects.create(name="Rações para cães")

        
class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Ração")
        self.product = Product.objects.create(
            name="Ração para cães",
            description="Ração para raças pequenas",
            price=Decimal('60.99'),
            stock=50,
            category=self.category
        )
        
    def test_product_creation(self):
        self.assertEqual(self.product.name, "Ração para cães")
        self.assertEqual(self.product.price, Decimal('60.99'))
        self.assertEqual(self.product.stock, 50)
        self.assertEqual(self.product.category, self.category)
        self.assertTrue(self.product.is_active)
        
    def test_product_str_method(self):
        self.assertEqual(str(self.product), "Ração para cães")
        
class ProductModelExtraTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="Teste")
        
    def test_name_black_validation(self):
        product = Product(
            name="",
            description="Algo",
            price=Decimal("5.00"),
            stock=1,
            category=self.cat
        )
        with self.assertRaises(ValidationError):
            product.full_clean()
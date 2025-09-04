from django.test import TestCase
from django.urls import reverse

from products.models import Category


class CategoryModelTest(TestCase):
    def setUp(self):
        """
        Configuração inicial para cada teste
        """
        self.category_data = {
            'name': 'Ração',
            'slug': 'racao'
        }
        
    def test_create_category_with_valid_data(self):
        category = Category.objects.create(**self.category_data)
        
        self.assertEqual(category.name, 'Ração')
        self.assertEqual(category.slug, 'racao')
        self.assertTrue(category.id)
        self.assertIsInstance(category.id, int)
        
    def test_create_category_without_slug(self):
        """
        Testa a criação de categoria sem slug (deve gerar autamaticamente).
        """
        category = Category.objects.create(name='Roupas Fêmeas')
        
        self.assertEqual(category.name, 'Roupas Fêmeas')
        self.assertEqual(category.slug, 'roupas-femeas')
        
    def test_create_category_with_special_characters(self):
        category = Category.objects.create(name='Roupas & Acessórios')
        
        self.assertEqual(category.name, 'Roupas & Acessórios')
        self.assertEqual(category.slug, 'roupas-acessorios')
        
    def test_create_category_with_accends(self):
        """
        Testa a criação com acentos no nome
        """
        category = Category.objects.create(name='Rações')
        
        self.assertEqual(category.name, 'Rações')
        self.assertEqual(category.slug, 'racoes')
        
    def test_str_method(self):
        category = Category.objects.create(name='Brinquedos')
        
        self.assertEqual(str(category), 'Brinquedos')
        
    def test_verbose_name(self):
        self.assertEqual(Category._meta.verbose_name, 'Categoria')
        self.assertEqual(Category._meta.verbose_name_plural, 'Categorias')
        
    def test_ordering(self):
        Category.objects.create(name='Zebra')
        Category.objects.create(name='Acessórios')
        Category.objects.create(name='Móveis')
        
        categories = Category.objects.all()
        names = [cat.name for cat in categories]
        
        self.assertEqual(names, ['Acessórios', 'Móveis', 'Zebra'])
        
    def test_get_absolute_url(self):
        category = Category.objects.create(name='Brinquedos')
        
        expected_url = reverse('category_detail', 
                               kwargs={'slug': category.slug}
                            )
        self.assertEqual(category.get_absolute_url(), expected_url)
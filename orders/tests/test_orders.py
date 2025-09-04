from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from django.utils import timezone
from datetime import datetime
import uuid

from products.models import Product, Category
from orders.models import Order, OrderItem, OrderStatus, PaymentMethod

User = get_user_model()

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            full_name='Test User',
            password='testpassword'
        )
    def test_create_order_valid(self):
        order = Order.objects.create(
            user=self.user,
            order_data=timezone.now().date(),
            status=OrderStatus.PENDENTE,
            total=Decimal('99.99'),
            shipping_address='Rua Exemplo, 123, Bairro',
            payment_method = PaymentMethod.PIX
        )
        self.assertIsInstance(order, Order)
        self.assertEqual(order.status, OrderStatus.PENDENTE)
        self.assertEqual(order.payment_method, PaymentMethod.PIX)
        self.assertGreater(order.total, 0)

    def test_pode_cancelar_quando_pendente(self):
        order = Order.objects.create(
            user=self.user,
            order_data=timezone.now().date(),
            status=OrderStatus.PENDENTE,
            total=Decimal('50.00'),
            shipping_address='Endereço teste',
            payment_method=PaymentMethod.BOLETO
        )
        self.assertTrue(order.pode_cancelar)
        
    def test_pode_cancelar_quando_enviado(self):
        order = Order.objects.create(
            user=self.user,
            order_data=timezone.now().date(),
            status=OrderStatus.ENVIADO,
            total=Decimal('75.00'),
            shipping_address='Endereço teste',
            payment_method=PaymentMethod.BOLETO
        )
        self.assertFalse(order.pode_cancelar)
        
    def test_can_cancel_property(self):
        pending_order = Order.objects.create(
            user=self.user,
            order_data=timezone.now().date(),
            status=OrderStatus.PENDENTE,
            total=Decimal('99.99'),
            shipping_address='Rua Exemplo, 123',
            payment_method=PaymentMethod.PIX
        )
        self.assertTrue(pending_order.pode_cancelar)
        
        delivery_order = Order.objects.create(
            user=self.user,
            order_data=timezone.now().date(),
            status=OrderStatus.ENTREGUE,
            total=Decimal('99.99'),
            shipping_address='Rua Exemplo, 123',
            payment_method=PaymentMethod.PIX
        )
        self.assertFalse(delivery_order.pode_cancelar)
        
    def test_cancel_method(self):
        order = Order.objects.create(
            user=self.user,
            order_data=timezone.now().date(),
            status=OrderStatus.PENDENTE,
            total=Decimal('99.99'),
            shipping_address='Rua Exemplo, 123',
            payment_method=PaymentMethod.PIX
        )
        order.cancel()
        order.refresh_from_db()
        self.assertEqual(order.status, OrderStatus.CANCELADO)
        
    def test_str_method(self):
        order = Order.objects.create(
            user=self.user,
            order_data=timezone.now().date(),
            status=OrderStatus.PENDENTE,
            total=Decimal('99.99'),
            shipping_address='Rua Exemplo, 123',
            payment_method=PaymentMethod.PIX
        )
        expected_str = f"Pedido {order.id} - {self.user.full_name} - Pendente"
        self.assertEqual(str(order), expected_str)
        
    def test_repr_method(self):
        order = Order.objects.create(
            user=self.user,
            order_data=timezone.now().date(),
            status=OrderStatus.PENDENTE,
            total=Decimal('99.99'),
            shipping_address='Rua Exemplo, 123',
            payment_method=PaymentMethod.PIX
        )
        expected_repr = f"<Pedido: {order.id}>"
        self.assertEqual(repr(order), expected_repr)
        
    def test_order_with_deifferent_payment_metohods(self):
        payment_methods = [
            PaymentMethod.CARTAO_CREDITO,
            PaymentMethod.CARTAO_DEBITO,
            PaymentMethod.BOLETO,
            PaymentMethod.PIX,
            PaymentMethod.DINHEIRO
        ]
        for payment_method in payment_methods:
            order = Order.objects.create(
                user=self.user,
                order_data=timezone.now().date(),
                status=OrderStatus.PENDENTE,
                total=Decimal('50.00'),
                shipping_address='Test Address, 456',
                payment_method=payment_method
            )
            self.assertEqual(order.payment_method, payment_method)
            
    def test_order_status_transitions(self):
        order = Order.objects.create(
            user=self.user,
            order_data=timezone.now().date(),
            status=OrderStatus.PENDENTE,
            total=Decimal('100.00'),
            shipping_address='Test Address, 789',
            payment_method=PaymentMethod.CARTAO_CREDITO
        )
        
        # Test status changes
        statuses = [
            OrderStatus.PROCESSANDO,
            OrderStatus.ENVIADO,
            OrderStatus.ENTREGUE
        ]
        for status in statuses:
            order.status = status
            order.save()
            order.refresh_from_db()
            self.assertEqual(order.status, status)
            
            

# Test Order Items
class OrderItemModelTest(TestCase):
    """Test cases for OrdeItem model"""
    
    def setUp(self):
        self.user = User.objects.create(
            email='test@example.com',
            full_name='Test User',
            password='testpass123'
        )
        
        self.category = Category.objects.create(name='Test Category')
        
        # Create products
        self.product1 = Product.objects.create(
            name='Test Product',
            price=Decimal('99.99'),
            stock=10,
            category=self.category
        )
        
        self.product2 = Product.objects.create(
            name='Test Product 2',
            description='Another test product',
            price=Decimal('49.99'),
            stock=5,
            category=self.category
        )
        
        
        # Create order
        self.order = Order.objects.create(
            user=self.user,
            status=OrderStatus.PENDENTE,
            total=Decimal('199.98'),
            shipping_address='Rua Test, 123, São Paulo, SP',
            payment_method=PaymentMethod.PIX
        )
        
        # Base order item data
        self.order_item_data = {
            'order':self.order,
            'product':self.product1,
            'quantity': 2,
            'unit_price': self.product1.price
        }
    
    def test_order_item_creation(self):
        """Test basic order item creation"""
        item = OrderItem.objects.create(**self.order_item_data)
        
        # Test field values
        self.assertIsInstance(item.id, uuid.UUID)
        self.assertEqual(item.order, self.order)
        self.assertEqual(item.product, self.product1)
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.unit_price, Decimal('99.99'))
        
        # Test timestamps
        self.assertLessEqual(item.created_at, item.updated_at)
        
        # Test that create_at and updated_at are closed (since both user auto_now=True)
        self.assertIsInstance(item.created_at, datetime)
        self.assertIsInstance(item.updated_at, datetime)
        time_diff = abs((item.updated_at - item.created_at).total_seconds())
        self.assertLess(time_diff, 1)
        self.assertGreaterEqual(item.updated_at, item.created_at)
        
    def test_order_item_uuid_uniqueness(self):
        """Test that each OrderItem gets a unique UUID"""
        item1 = OrderItem.objects.create(**self.order_item_data)
        
        # Create second item with different product
        item_data2 = self.order_item_data.copy()
        item_data2['product'] = self.product2
        item2 = OrderItem.objects.create(**item_data2)
        
        self.assertNotEqual(item1.id, item2.id)
        self.assertIsInstance(item1.id, uuid.UUID)
        self.assertIsInstance(item2.id, uuid.UUID)
        
    def test_order_item_str_representation(self):
        """Test order item sring representation"""
        item = OrderItem.objects.create(**self.order_item_data)
        # Note: The original model has a typo "Product" instead of "Product"
        expected_str = f"2x Product {self.product1.id} (Order {self.order.id})"
        self.assertEqual(str(item), expected_str)
        
    def test_order_item_repr_representation(self):
        item = OrderItem.objects.create(**self.order_item_data)
        # Note: The original model has missing space in repr
        expected_repr = f"<OrderItem: {item.id}>"
        self.assertEqual(repr(item), expected_repr)
    
    def test_quantity_positive_integer_validation(self):
        # Test valid quantities
        valid_quantities = [1, 5, 10, 100, 150]
        for quantity in valid_quantities:
            item = OrderItem(
                order=self.order,
                product=self.product1,
                quantity=quantity,
                unit_price=self.product1.price
            )
            try:
                item.full_clean()
            except ValidationError as e:
                self.fail(f"Quantidade {quantity} deveri ser válida. Erro {e}")
                
    def test_quantity_validation(self):
        """Test quantity validation (minimum value)"""
        item_data = self.order_item_data.copy()
        item_data['quantity'] = 0 # Invalid: below minimum
        
        item = OrderItem(**item_data)
        with self.assertRaises(ValidationError):
            item.full_clean()
            
    def test_unit_price_validation(self):
        """Test unit price validation (minimum value)"""
        item_data = self.order_item_data.copy()
        item_data['unit_price'] = Decimal('0.00') # Invalid: below minimum
        
        item = OrderItem(**item_data)
        with self.assertRaises(ValidationError):
            item.full_clean()
            
    def test_subtotal_property(self):
        item = OrderItem.objects.create(**self.order_item_data)
        expected_subtotal = Decimal('2') * Decimal('99.99') # Quantity * unit_price
        self.assertEqual(item.subtotal, expected_subtotal)
        
    def test_unique_together_constraint(self):
        """Test unique together constraint (order, product)"""
        # Create first item
        OrderItem.objects.create(**self.order_item_data)
        
        # Try to cretate duplicate item (same order, same product)
        with self.assertRaises(IntegrityError):
            OrderItem.objects.create(**self.order_item_data)
            
    def test_order_item_save_updates_order_total(self):
        # Initial order total
        inital_total = self.order.total
        
        # Create order item
        item = OrderItem.objects.create(**self.order_item_data)
        self.order.refresh_from_db()
        expected_total = item.subtotal
        self.assertEqual(self.order.total, expected_total)
        
        
    def test_multiple_order_items_total_calculation(self):
        item1 = OrderItem.objects.create(**self.order_item_data)
        
        product2 = Product.objects.create(
            name='Test Product 2 - unique',
            description='Another test product',
            price=Decimal('25.00'),
            stock=5,
            category=self.category
        )
        
        item2 = OrderItem.objects.create(
            order=self.order,
            product=product2,
            quantity=3,
            unit_price=Decimal('25.00')
        )
        
        self.order.refresh_from_db()
        
        expected_total = item1.subtotal + item2.subtotal
        self.assertEqual(self.order.total, expected_total)
         
         
class OrderItemModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # 1) cria um usuário (custom user pode exigir outros campos)
        cls.user = User.objects.create_user(
            email='testuser@example.com',
            full_name='Jadson Silva',
            password='password123',
        )

        # 2) cria uma categoria para vincular ao produto
        cls.category = Category.objects.create(name='Teste Categoria')

        # 3) cria o pedido com todos os campos obrigatórios
        cls.order = Order.objects.create(
            user             = cls.user,
            status           = OrderStatus.PENDENTE,
            total            = Decimal('0.01'),
            shipping_address = "Rua Exemplo, 123",
            payment_method   = PaymentMethod.PIX,
        )

        # 4) cria o produto preenchendo *tudo* que não aceita NULL
        cls.product1 = Product.objects.create(
            name        = "Produto X",
            description = "Descrição do Produto X",
            price       = Decimal('50.00'),
            stock       = 10,
            category    = cls.category,
            # status, image e is_active têm defaults, então não são obrigatórios
        )
        
    def test_quantity_positive_integer_validation(self):
       """
       Não deve lançar ValidationError para quantidades inteiras positivas.
       """
       valid_quantities = [1, 5, 10, 100, 150]
       for qty in valid_quantities:
           item = OrderItem(
               order      = self.order,
               product    = self.product1,
               quantity   = qty,
               unit_price = self.product1.price,
           )
           try:
               item.full_clean()
           except ValidationError as e:
               self.fail(f"Quantidade {qty} deveria ser válida, mas falhou: {e}")

    def test_quantity_zero_negative_or_non_integer_raises(self):
        """
        Deve lançar ValidationError para 0, negativos e não-inteiros.
        """
        invalid_quantities = [0, -1, -10, 2.5, "dez"]
        for qty in invalid_quantities:
            item = OrderItem(
                order      = self.order,
                product    = self.product1,
                quantity   = qty,
                unit_price = self.product1.price,
            )
            with self.assertRaises(ValidationError, msg=f"Quantidade {qty} deveria falhar"):
                item.full_clean()
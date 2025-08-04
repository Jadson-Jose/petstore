from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils import timezone
from orders.models import Order, OrderStatus, PaymentMethod


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='12345'
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
        expected_str = f"Pedido {order.id} - {self.user.username} - Pendente"
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
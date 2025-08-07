from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal
import uuid

from products.models import Product

class OrderStatus(models.TextChoices):
    """Choices para status do pedido usando TextChoices (Django 3..+)"""
    PENDENTE = 'pendente', 'Pendente'
    PROCESSANDO = 'processando', 'Processando'
    ENVIADO = 'enviado', 'Enviado'
    ENTREGUE = 'entregue', 'Entregue'
    CANCELADO = 'cancelado', ' Cancelado'
    
class PaymentMethod(models.TextChoices):
    CARTAO_CREDITO = 'cartão_crédito', 'Cartão de Crédito'
    CARTAO_DEBITO = 'cartão_debito', 'Cartão de Débito'
    BOLETO = 'boleto', 'Boleto Bancário'
    PIX = 'pix', 'PIX'
    DINHEIRO = 'dinheiro', 'Dinheiro'
    
class Order(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Identificador único do pedido"
    )
    
    # Relacionamento com User (pode ser costumizado para seu modelo de usuátio)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, # PROTECT evita exclusão acidental
        related_name='pedidos',
        verbose_name="Usuário",
        help_text="Usuário que realizou o pedido",
    )
    
    # Timestamps
    order_data = models.DateField(
        default=timezone.now,
        verbose_name='Data do Pedido',
        help_text="Data e hora que o pedido foi realizado"
    )
    
    # Status com choices
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        verbose_name="Status",
        help_text="Status atual do pedido"
    )
    
    # Valor total com validação
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Total",
        help_text="Valor total do pedido"
    )
    
    # Endereço de envio
    shipping_address = models.TextField(
        max_length=500,
        verbose_name="Endereço de Envio",
        help_text="Endereço completo para envio do pedido"
    )
    
    # Método de pagamento
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        verbose_name="Método de Pagamento", 
        help_text="Método de pagamento utilizado"
    )
    
    # Campos de auditoria
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-order_data']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['order_data']),
            models.Index(fields=['status']),
        ]
        
    def __str__(self):
        return f"Pedido {self.id} - {self.user.username} - {self.get_status_display()}"
    
    def __repr__(self):
        return f"<Pedido: {self.id}>"
    
    @property
    def pode_cancelar(self):
        """Verifica se o pedido pode ser cancelado"""
        return self.status in [OrderStatus.PENDENTE, OrderStatus.PROCESSANDO]
    
    def cancel(self):
        """Cancela o pedido se possível"""
        if self.pode_cancelar:
            self.status = OrderStatus.CANCELADO
            self.save()
            
    def calculate_total(self):
        return sum(item.subtotal for item in self.items.all())
    
class OrderItem(models.Model):
    """
    Individual items within an order
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Identificador único para intens do pedido."
    )
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Ordem',
        help_text="Pedido ao qual este item pertence"
    )
    
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name="Produto",
        help_text="Pedido do produto"
    )
    
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Quantidade",
        help_text="Quantidade de produto no pedido"
    )
    
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Unit Price",
        help_text="Price per unit at the same time of purchase (important for history)"
    )
    
    # Audit fields
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )
    
    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        ordering = ['order', 'created_at']
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['product_id'])
        ]
        
        # Ensure no duplicate products in the same order
        unique_together = ['order', 'product']
        
    def __str__(self):
        return f"{self.quantity}x Product {self.product_id} (Order {self.order.id})"
    
    def __repr__(self):
        return f"<OrderItem: {self.id}>"
    
    @property
    def subtotal(self):
        """Calculate subtotal for this item"""
        return self.quantity * self.unit_price
    
    def save(self, *args, **kwargs):
        """Override save to update order total when item changes"""
        super().save(*args, **kwargs)
        
        # Optionally update order total automatically
        self.order.total = self.order.calculate_total()
        self.order.save()
    
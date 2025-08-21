from django.db import models

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
        ('rejected', 'Recusado'),
        ('refunded', 'Reembolsado'),
    ]
    
    METHOD_CHOICES = [
        ('credit_card', 'Cartão de Crédito'),
        ('boleto', 'Boleto'),
        ('pix', 'Pix'),
    ]
    
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="payments"
    )
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return f"Pagamento {self.id} - {self.status}"
    
    
class Invoid(models.Model):
    NFE_STATUS_CHOICES = [
        ('authorized', 'Autorizada'),
        ('canceled', 'Cancelada'),
        ('rejected', 'Rejeitada'),
    ]
    
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="invoices"
    )
    access_key = models.CharField(max_length=44, unique=True) # Chace de acesso da NFe
    number = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=NFE_STATUS_CHOICES, default='authorized')
    xml_file = models.FileField(upload_to="invoices/", null=True, blank=True)
    issue_at = models.DateTimeField()
    authorized_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Nota fiscal {self.number}  - {self.status}"

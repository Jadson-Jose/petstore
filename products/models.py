from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal


class CustomUserManager(BaseUserManager):
    """Gerenciador personalizado para o modelo User sem campo username"""

    def _create_user(self, email, password, **extra_fields):
        """Cria e salva um usuário com email e senha"""
        if not email:
            raise ValueError(_('O email deve ser definido'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superusuário deve ter is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superusuário deve ter is_superuser=True.'))

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Modelo de usuário personalizado"""
    # Remover o campo username padrão
    username = None

    # Campos obrigatórios
    email = models.EmailField(_('email address'), unique=True)
    nome_completo = models.CharField(_('nome completo'), max_length=150)

    # Campos adicionais
    endereco = models.TextField(_('endereço'), blank=True)
    telefone = models.CharField(_('telefone'), max_length=20, blank=True)
    data_cadastro = models.DateTimeField(_('data de cadastro'), auto_now_add=True)
    is_admin = models.BooleanField(
        _('administrador'),
        default=False,
        help_text=_('Designa se o usuário tem privilégios administrativos')
    )

    # Definir o email como campo de login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_completo']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('usuário')
        verbose_name_plural = _('usuários')
        ordering = ['-data_cadastro']

    def __str__(self):
        return self.nome_completo or self.email

    def get_full_name(self):
        return self.nome_completo

    def get_short_name(self):
        return self.nome_completo.split()[0] if self.nome_completo else self.email.split('@')[0]


class Categoria(models.Model):
    """Modelo para categorias de produtos"""
    nome = models.CharField(_('nome'), max_length=100, unique=True)
    descricao = models.TextField(_('descrição'), blank=True)
    ativo = models.BooleanField(_('ativo'), default=True)
    data_criacao = models.DateTimeField(_('data de criação'), auto_now_add=True)

    class Meta:
        verbose_name = _('categoria')
        verbose_name_plural = _('categorias')
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Product(models.Model):
    """Modelo para produtos da petshop"""
    
    # Campos básicos do produto
    nome = models.CharField(_('nome'), max_length=200)
    descricao = models.TextField(_('descrição'), blank=True)
    
    # Preço e estoque
    preco = models.DecimalField(
        _('preço'), 
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    estoque = models.PositiveIntegerField(_('quantidade em estoque'), default=0)
    
    # Categoria e classificação
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('categoria'),
        related_name='produtos'
    )
    
    # Campos específicos para petshop
    marca = models.CharField(_('marca'), max_length=100, blank=True)
    peso = models.DecimalField(
        _('peso (kg)'), 
        max_digits=6, 
        decimal_places=3, 
        blank=True, 
        null=True
    )
    idade_recomendada = models.CharField(
        _('idade recomendada'),
        max_length=50,
        blank=True,
        help_text=_('Ex: Filhote, Adulto, Idoso, Todas as idades')
    )
    especie = models.CharField(
        _('espécie'),
        max_length=50,
        blank=True,
        help_text=_('Ex: Cão, Gato, Pássaro, Peixe, etc.')
    )
    
    # Imagens e mídia
    imagem_principal = models.ImageField(
        _('imagem principal'), 
        upload_to='products/images/', 
        blank=True, 
        null=True
    )
    
    # Status e controle
    ativo = models.BooleanField(_('ativo'), default=True)
    destaque = models.BooleanField(_('produto em destaque'), default=False)
    promocao = models.BooleanField(_('em promoção'), default=False)
    preco_promocional = models.DecimalField(
        _('preço promocional'),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    # Metadados
    codigo_barras = models.CharField(
        _('código de barras'), 
        max_length=50, 
        blank=True, 
        unique=True,
        null=True
    )
    sku = models.CharField(
        _('SKU'), 
        max_length=50, 
        blank=True, 
        unique=True,
        null=True,
        help_text=_('Stock Keeping Unit - Código interno do produto')
    )
    
    # Timestamps
    data_criacao = models.DateTimeField(_('data de criação'), auto_now_add=True)
    data_atualizacao = models.DateTimeField(_('data de atualização'), auto_now=True)

    class Meta:
        verbose_name = _('produto')
        verbose_name_plural = _('produtos')
        ordering = ['-data_criacao']
        indexes = [
            models.Index(fields=['nome']),
            models.Index(fields=['categoria']),
            models.Index(fields=['ativo']),
            models.Index(fields=['destaque']),
        ]

    def __str__(self):
        return self.nome

    def get_preco_final(self):
        """Retorna o preço final considerando promoção"""
        if self.promocao and self.preco_promocional:
            return self.preco_promocional
        return self.preco

    def get_desconto_percentual(self):
        """Calcula o percentual de desconto se em promoção"""
        if self.promocao and self.preco_promocional and self.preco > 0:
            desconto = ((self.preco - self.preco_promocional) / self.preco) * 100
            return round(desconto, 2)
        return 0

    def esta_em_estoque(self):
        """Verifica se o produto está em estoque"""
        return self.estoque > 0

    def save(self, *args, **kwargs):
        """Override do save para validações extras"""
        # Se não está em promoção, limpar preço promocional
        if not self.promocao:
            self.preco_promocional = None
        
        # Validar que preço promocional é menor que preço normal
        if self.promocao and self.preco_promocional and self.preco_promocional >= self.preco:
            raise ValueError(_('Preço promocional deve ser menor que o preço normal'))
        
        super().save(*args, **kwargs)


class ImagemProduto(models.Model):
    """Modelo para imagens adicionais dos produtos"""
    produto = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='imagens_adicionais',
        verbose_name=_('produto')
    )
    imagem = models.ImageField(_('imagem'), upload_to='products/gallery/')
    descricao = models.CharField(_('descrição'), max_length=200, blank=True)
    ordem = models.PositiveIntegerField(_('ordem'), default=0)
    
    class Meta:
        verbose_name = _('imagem do produto')
        verbose_name_plural = _('imagens dos produtos')
        ordering = ['ordem', 'id']

    def __str__(self):
        return f'{self.produto.nome} - Imagem {self.id}'
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O email deve ser definido')
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
            raise ValueError('Superusuário deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário deve ter is_superuser=True.')
        
        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    # Remover username padrão
    username = None
    
    # Campos obrigatórios
    email = models.EmailField(_('email'), unique=True)
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
    
    # Corrigir conflitos de relacionamento
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name="users_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name="users_user_set",
        related_query_name="user",
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_completo']
    
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = _('usuário')
        verbose_name_plural = _('usuários')
        ordering = ['-data_cadastro']
    
    def __str__(self):
        return self.nome_completo or self.email
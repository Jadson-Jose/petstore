from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """
    Manager customizado para o modelo User que usa email ao invés de username.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Cria e salva um usuário com o email e senha fornecidos.
        """
        if not email:
            raise ValueError("O campo email é obrigatório.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Cria e salva um superusuário com o email e senha fornecidos.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser deve ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser deve ter is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Modelo de usuário customizado que estende o AbstractUser do Django.
    Inclui campos adicionais para o sistema de petshop.
    """

    username = None
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        help_text="Endereço de e-mail único do usuário",
    )

    name = models.CharField(
        max_length=150,
        verbose_name="Nome Completo",
        help_text="Nome completo do usuário",
    )

    address = models.TextField(
        blank=True,
        verbose_name="Endereço",
        help_text="Endereço de entrega padrão do usuário",
    )

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Número de telefone deve estar no formato: '+999999999'. \
            Até 15 dígitos permitidos.",
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        verbose_name="Telefone",
        help_text="Número de telefone de contato",
    )

    registration_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data de Cadastro",
        help_text="Data e hora do registro do usuário",
    )

    is_admin = models.BooleanField(
        default=False,
        verbose_name="Administrador",
        help_text="Indica se o usuário tem privilégios administrativos",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ["-registration_date"]

    def __str__(self):
        return f"{self.name} ({self.email})"

    def get_full_name(self):
        """Retorna o nome completo do usuário."""
        return self.name

    def get_short_name(self):
        """Retorna o primeiro nome do usuário."""
        return self.name.split()[0] if self.name else self.email

    def save(self, *args, **kwargs):
        """Override do save para garantir que email seja sempre lowercase."""
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)

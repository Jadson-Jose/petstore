from django.utils import timezone
from django.test import TestCase
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
    """Testes para o modelo de usuário customizado"""

    def setUp(self):
        """Configuração inicial para os testes"""
        self.user_data = {
            "email": "test@example.com",
            "name": "Jadson Silva",
            "address": "Rua das Flores, 123, São Paluo, SP",
            "phone": "+5511999999999",
            "password": "senha123",
        }

    def test_create_user_basic(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.name, "Jadson Silva")
        self.assertTrue(user.check_password("senha123"))
        return super().setUp()

    def test_create_user_with_valid_data(self):
        email = "Teste@Example.com"
        name = "Teste Usuário"
        password = "senha123"
        user = User.objects.create_user(
            email=email,
            name=name,
            password=password
        )
        """erifica se o email foi transformado
           para lowercase e outros atributos.
        """
        self.assertEqual(user.email, email.lower())
        self.assertEqual(user.name, name)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_admin)
        self.assertTrue(user.registration_date <= timezone.now())

    def test_create_user_without_email_raises_error(self):
        with self.assertRaises(ValueError) as context:
            User.objects.create_user(
                email=None,
                password="senha",
                name="Teste"
            )
        self.assertIn("O campo email é obrigatório.", str(context.exception))

    def test_create_superuser_with_valid_date(self):
        email = "admin@example.com"
        name = "Adminstrador"
        password = "senhaadmin"
        admin = User.objects.create_superuser(
            email=email,
            name=name,
            password=password,
        )
        """Verifica se os flags do superusuário estão corretos."""
        self.assertEqual(admin.email, email.lower())
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_admin)

    def test_create_superuser_invalid_is_staff(self):
        email = "admin@example.com"
        name = "Administrador"
        password = "senhaadmin"
        with self.assertRaises(ValueError) as context:
            User.objects.create_superuser(
                email=email,
                password=password,
                name=name,
                is_staff=False
            )
        self.assertIn(
            "Superuser deve ter is_staff=True",
            str(context.exception)
        )

    def test_create_superuser_invalid_is_superuser(self):
        email = "admin@example.com"
        name = "Administrador"
        password = "senhaadmin"
        with self.assertRaises(ValueError) as context:
            User.objects.create_superuser(
                email=email,
                password=password,
                name=name,
                is_superuser=False
            )
        self.assertIn(
            "Superuser deve ter is_superuser=True",
            str(context.exception)
        )

    def test_get_full_name_returns_name(self):
        email = "user@email.com"
        name = "Jadson Silva"
        user = User.objects.create_user(
            email=email,
            password="password",
            name=name,
        )
        self.assertEqual(user.get_full_name(), name)

    def test_get_short_name_returns_first_name(self):
        email = "user@email.com"
        name = "Jadson Silva"
        user = User.objects.create_user(
            email=email,
            password="password",
            name=name,
        )
        self.assertEqual(user.get_short_name(), "Jadson")

        """Quando o campo está vazio, deve retornar o email"""
        user_empty = User.objects.create_user(
            email="vazio@example.com",
            password="password",
            name=""
        )
        self.assertEqual(user_empty.get_short_name(), "vazio@example.com")

    def test_str_method_returns_name_and_email(self):
        email = "user@example.com"
        name = "Jadson Silva"
        user = User.objects.create_user(
            email=email,
            password="password",
            name=name,
        )
        expective_str = f"{name} ({email.lower()})"
        self.assertEqual(str(user), expective_str)

    def test_email_is_lowercase_on_save(self):
        email = "User@Domain.com"
        user = User.objects.create_user(
            email=email,
            password="senha",
            name="Teste"
        )
        """Verifica se o email foi salve em lowercase"""
        self.assertEqual(user.email, email.lower())
        """Altera o email para uppercase e salva novamente"""
        new_email = "NEW@EMAIL.COM"
        user.email = new_email
        user.save()
        self.assertEqual(user.email, new_email.lower())

    def test_phone_field_validation(self):
        email = "phone@example.com"
        usuario = User.objects.create_user(
            email=email,
            password="password",
            name="Teste phone"
        )
        """Testa com um número de phone válido"""
        usuario.phone = '+12345678901'
        try:
            usuario.full_clean()
        except ValueError:
            self.fail(
                "full_clean() levantou ValidationError inesperadamente,"
                "com um phone válido!"
            )
        """Testa com um número de phone inválido e espera que seja
           levantada uma exceção"""
        usuario.phone = "phoneinvalido"
        with self.assertRaises(ValidationError):
            usuario.full_clean()

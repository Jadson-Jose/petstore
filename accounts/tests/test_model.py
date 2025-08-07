import pytest
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_str_representation():
    user = User.objects.create_user(
        email='jadson@email.com',
        password='teste123',
        full_name='Jadson Jose'
    )
    assert str(user) == 'jadson@email.com'
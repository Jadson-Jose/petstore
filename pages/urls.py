# pages/urls.py
from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    # Adicione outras URLs conforme necessário
    # path('sobre/', views.about, name='about'),
    # path('contato/', views.contact, name='contact'),
]
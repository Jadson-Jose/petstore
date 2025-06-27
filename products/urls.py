from django.urls import path
from . import views

app_name = 'products'  # 🔑 NAMESPACE CRÍTICO

urlpatterns = [
    path('', views.product_list, name='list'),
    path('<slug:slug>/', views.product_detail, name='detail'),
    # Adicione outras URLs do app products aqui
]
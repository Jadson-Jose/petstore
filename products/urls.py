from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_products, name='list_products'),
    path('products/<int:product_id>/', views.detail_product, name='detail_product'),
]

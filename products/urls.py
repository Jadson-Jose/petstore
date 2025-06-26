from django.urls import path
from .views import CategoryProductListView, ProductListView, ProductDetailView
from .views import home

urlpatterns = [
    path("", home, name="home"),
    path("produtos/", ProductListView.as_view(), name="product_list"),
    path("produtos/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("categoria/<int:category_id>/", CategoryProductListView.as_view(), name="category_products",),
]

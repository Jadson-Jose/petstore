from django.shortcuts import render, get_object_or_404

from .models import Product


def list_products(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'products/list.html', {'products': products})

def detail_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/detail.html', {'product': product})

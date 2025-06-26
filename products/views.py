from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render
from .models import Product, Category


def home(request):
    # Obter categorias em destaque
    featured_categories = Category.objects.filter(featured=True)[:4]

    # Obter produtos populares (mais vendidos)
    popular_products = Product.objects.filter(active=True).order_by('-sold')[:8]

    context = {
        'featured_categories': featured_categories,
        'popular_products': popular_products,
        'categories': Category.objects.all(),
    }
    return render(request, 'products/home.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.filter(active=True).order_by('-created_at')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(
            category=self.object.category,
            active=True
        ).exclude(id=self.object.id)[:4]
        return context


class CategoryProductListView(ListView):
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            id=self.kwargs['category_id']
        )
        return Product.objects.filter(
            category=self.category,
            active=True
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.category
        return context

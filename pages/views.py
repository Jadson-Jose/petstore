from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

class HomeView(TemplateView):
    template_name = 'pages/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'site_name': 'PetStore',
            'featured_products': [],
            'categories': [],
            'total_products': 500,
            'happy_pets': 15000,
        })
        return context


class NewsletterView(TemplateView):
    template_name = 'pages/newsletter.html'


@csrf_exempt
def newsletter_subscribe(request):
    """Handle newsletter subscription via AJAX"""
    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                email = data.get('email')
            else:
                email = request.POST.get('email')
            
            if email:
                # Here you would typically save to database
                # NewsletterSubscriber.objects.create(email=email)
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Obrigado! Você foi inscrito em nossa newsletter.'
                    })
                else:
                    messages.success(request, 'Obrigado! Você foi inscrito em nossa newsletter.')
                    return redirect('pages:home')
            else:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Por favor, forneça um email válido.'
                    })
                else:
                    messages.error(request, 'Por favor, forneça um email válido.')
                    return redirect('pages:home')
                    
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': 'Erro interno. Tente novamente.'
                })
            else:
                messages.error(request, 'Erro interno. Tente novamente.')
                return redirect('pages:home')
    
    return redirect('pages:home')


class ProductsView(TemplateView):
    template_name = 'pages/products.html'


class CategoriesView(TemplateView):
    template_name = 'pages/categories.html'


class AboutView(TemplateView):
    template_name = 'pages/about.html'


class ContactView(TemplateView):
    template_name = 'pages/contact.html'

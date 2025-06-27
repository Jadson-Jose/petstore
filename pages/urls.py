from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('sobre/', views.AboutView.as_view(), name='about'),
    path('contato/', views.ContactView.as_view(), name='contact'),
    
    # Add newsletter URL
    path('newsletter/', views.NewsletterView.as_view(), name='newsletter'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    
    # Add other common URLs that might be referenced
    path('produtos/', views.ProductsView.as_view(), name='products'),
    path('categorias/', views.CategoriesView.as_view(), name='categories'),
]
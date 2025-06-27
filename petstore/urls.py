from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('produtos/', include('products.urls')),  # assuming you have a products app
    path('usuarios/', include('users.urls')),     # assuming you have a users app
    
    # Add homepage URL - Option 1: Using TemplateView
    path('', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    
    # OR Option 2: Create a dedicated view (recommended)
    # path('', include('pages.urls')),  # if you create a pages app
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
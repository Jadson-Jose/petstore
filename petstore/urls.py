from django.contrib import admin
from django.urls import include,  path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include("home.urls")),
    path('categories/', include('category.urls')),
]

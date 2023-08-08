
from django.contrib import admin
from django.urls import path, include
from NinazHairline.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('NinazHairline.urls')),

    path('accounts/', include('allauth.urls')),

    
]

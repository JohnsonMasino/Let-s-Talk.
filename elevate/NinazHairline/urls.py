from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.home, name=""),
    
    path('dashboard/', views.dashboard, name='dashboard'),

    path('service/<str:pk>/', views.service, name='service'),

]


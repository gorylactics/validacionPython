from django.urls import path
from . import views

urlpatterns = [
    path('' , views.index),
    path('registrar/', views.registrar),
    path('login/', views.log),
    path('success/', views.success),
    path('logout/', views.logout)
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('crear/', views.registrar_evento, name='crear_evento'),
    path('registro-exitoso/', views.registro_exitoso, name='registro_exitoso'),
]

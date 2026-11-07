from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('portada/', views.portada, name='portada'), 
    path ('diccionario/', views.diccionario, name='diccionario'),
    path('diccionario/<int:id_termino>/', views.detalle_termino, name='detalle_termino'),
]
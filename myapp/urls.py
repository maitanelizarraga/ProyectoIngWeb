from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('portada/', views.portada, name='portada'), 
    path ('diccionario/', views.diccionario, name='diccionario'),
    path('diccionario/<int:id_termino>/', views.detalle_termino, name='detalle_termino'),
    path('inicio/', views.inicio, name='inicio'),
    path('addPalabra/', views.addPalabra, name='addPalabra'),
    path('ramasDerecho/', views.ramasDerecho, name='ramasDerecho'),
    path('galeria/', views.galeria, name='galeria'),
    path('nuevas/', views.nuevas, name='nuevas'),
]
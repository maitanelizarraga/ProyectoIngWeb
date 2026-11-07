from django.shortcuts import render, get_object_or_404
from .models import RamaDerecho, Termino
from django.http import HttpResponse

# Create your views here.
def index(request):
    context = {
        'ramas_publico': RamaDerecho.objects.filter(tipo='publico'),
        'ramas_privado': RamaDerecho.objects.filter(tipo='privado'),
        'palabras': Termino.objects.all()[:5],
    }
    return render(request, 'inicio.html', context)

def diccionario(request):
    terminos = Termino.objects.all()
    context = {'terminos': terminos}
    return render(request, 'myapp/diccionario.html', context)

def detalle_termino(request, id_termino):
    termino = get_object_or_404(Termino, pk=id_termino)
    return render(request, 'myapp/detalle_termino.html', {'termino': termino})
from django.shortcuts import render, get_object_or_404
from .models import Termino
from django.http import HttpResponse

# Create your views here.
def index(request):
    ultimos_terminos = Termino.objects.order_by('-fecha_creacion')[:5]
    context = {'ultimos_terminos': ultimos_terminos}   
    return render(request, 'myapp/index.html', context)

def diccionario(request):
    terminos = Termino.objects.all()
    context = {'terminos': terminos}
    return render(request, 'myapp/diccionario.html', context)

def detalle_termino(request, id_termino):
    termino = get_object_or_404(Termino, pk=id_termino)
    return render(request, 'myapp/detalle_termino.html', {'termino': termino})

# views.py
def portada(request):
    return render(request, 'myapp/portada.html')
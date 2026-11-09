from django.shortcuts import render, get_object_or_404
from .models import TerminoGeneral, Subrama
from django.http import HttpResponse


def index(request):
    ultimos_terminos = TerminoGeneral.objects.order_by('-created_at')[:5]
    context = {'ultimos_terminos': ultimos_terminos}
    return render(request, 'myapp/index.html', context)


def diccionario(request):
    terminos = list(TerminoGeneral.objects.all())

    # Ordenar alfabéticamente
    terminos.sort(key=lambda t: t.termino.casefold())

    # Agrupar los términos por su primera letra
    grupos = []
    for termino in terminos:
        letra = termino.termino[0].upper()

        if not grupos or grupos[-1]['letra'] != letra:
            grupos.append({
                'letra': letra,
                'terminos': []
            })

        grupos[-1]['terminos'].append(termino)

    context = {'grupos': grupos}

    return render(request, 'myapp/diccionario.html', context)


def detalle_termino(request, id_termino):
    termino = get_object_or_404(TerminoGeneral, pk=id_termino)
    return render(request, 'myapp/detalle_termino.html', {'termino': termino})


def portada(request):
    return render(request, 'myapp/portada.html')


def inicio(request):
    ramas_publico = Subrama.objects.filter(rama__nombre='Derecho Público')
    ramas_privado = Subrama.objects.filter(rama__nombre='Derecho Privado')
    palabras = TerminoGeneral.objects.order_by('-created_at')[:5]
    context = {
        'ramas_publico': ramas_publico,
        'ramas_privado': ramas_privado,
        'palabras': palabras,
    }
    return render(request, 'myapp/inicio.html', context)

def addPalabra(request):
    if request.method == 'POST':
        termino = request.POST.get('termino')
        definicion = request.POST.get('definicion')
        rama_id = request.POST.get('rama')
        subrama_id = request.POST.get('subrama')

        # Crear un nuevo objeto TerminoGeneral
        nuevo_termino = TerminoGeneral(
            termino=termino,
            definicion=definicion,
            rama_id=rama_id,
            subrama_id=subrama_id
        )
        nuevo_termino.save()

        return render(request, 'myapp/addPalabra.html', {'mensaje': 'Palabra añadida correctamente.'})

    return render(request, 'myapp/addPalabra.html')
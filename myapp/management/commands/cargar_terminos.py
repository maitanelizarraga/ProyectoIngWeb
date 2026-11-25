import json
from pathlib import Path

from django.core.management.base import BaseCommand

from myapp.models import Subrama, TerminoGeneral


class Command(BaseCommand):
    help = 'Carga los términos del diccionario desde myapp/data/terminos.json'

    def handle(self, *args, **options):
        ruta = Path(__file__).resolve().parents[2] / 'data' / 'terminos.json'
        datos = json.loads(ruta.read_text(encoding='utf-8'))

        campos = [f.name for f in TerminoGeneral._meta.get_fields()]
        tiene_ejemplo = 'ejemplo' in campos
        tiene_relacionados = 'relacionados' in campos

        creados = 0
        ya_existian = 0

        for d in datos:
            if TerminoGeneral.objects.filter(termino__iexact=d['termino']).exists():
                ya_existian += 1
                continue

            termino = TerminoGeneral(termino=d['termino'], definicion=d['definicion'])
            if tiene_ejemplo:
                termino.ejemplo = d['ejemplo']
            if tiene_relacionados:
                termino.relacionados = d['relacionados']
            termino.save()

            for nombre in d['subramas']:
                try:
                    termino.subramas.add(Subrama.objects.get(nombre=nombre))
                except Subrama.DoesNotExist:
                    self.stdout.write(f'  Aviso: no existe la subrama "{nombre}" ({d["termino"]})')
            creados += 1

        self.stdout.write(self.style.SUCCESS(
            f'Creados: {creados}. Ya existían (no se tocan): {ya_existian}.'))
        if not tiene_ejemplo or not tiene_relacionados:
            self.stdout.write('Nota: el modelo no tiene campo "ejemplo" y/o "relacionados", '
                              'esos datos no se han guardado.')

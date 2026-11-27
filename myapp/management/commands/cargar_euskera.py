import json
from pathlib import Path

from django.core.management.base import BaseCommand

from myapp.models import TerminoGeneral


class Command(BaseCommand):
    help = 'Añade la traducción al euskera a los términos ya cargados (myapp/data/terminos_eu.json)'

    def handle(self, *args, **options):
        ruta = Path(__file__).resolve().parents[2] / 'data' / 'terminos_eu.json'
        datos = json.loads(ruta.read_text(encoding='utf-8'))

        actualizados = 0
        for d in datos:
            try:
                termino = TerminoGeneral.objects.get(termino__iexact=d['termino'])
            except TerminoGeneral.DoesNotExist:
                self.stdout.write(f'  Aviso: no existe en la base de datos "{d["termino"]}"')
                continue

            termino.termino_eu = d['termino_eu']
            termino.definicion_eu = d['definicion_eu']
            termino.ejemplo_eu = d['ejemplo_eu']
            termino.relacionados_eu = d['relacionados_eu']
            termino.save()
            actualizados += 1

        self.stdout.write(self.style.SUCCESS(f'Términos con euskera: {actualizados}'))

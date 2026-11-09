from django.db import migrations


RAMAS = [
    ('Derecho Público', 'Regula las relaciones entre el Estado y las personas.'),
    ('Derecho Privado', 'Regula las relaciones entre dos o más personas.'),
]

SUBRAMAS = {
    'Derecho Público': [
        'Derecho Administrativo',
        'Derecho Financiero y Tributario',
        'Derecho Constitucional',
        'Derecho Penal',
        'Derecho Penitenciario',
        'Derecho Procesal',
        'Derecho Internacional Público',
    ],
    'Derecho Privado': [
        'Derecho Civil',
        'Derecho Mercantil',
        'Derecho Laboral',
        'Derecho Internacional Privado',
    ],
}

CONCEPTOS = [
    ('Jurisdicción',      'Potestad de juzgar y hacer ejecutar lo juzgado.',         'procesal'),
    ('Competencia',       'Atribución legal a un órgano para conocer un asunto.',    'procesal'),
    ('Sujeto de derecho', 'Persona física o jurídica titular de derechos y deberes.','general'),
    ('Obligación',        'Vínculo jurídico por el que una parte debe dar, hacer o no hacer algo.', 'general'),
    ('Responsabilidad',   'Deber de asumir las consecuencias de un acto u omisión.', 'general'),
]

TERMINOS_GENERALES = [
    ('Norma jurídica',        'Regla de conducta obligatoria impuesta por el Estado.',             'Kelsen',       'Teoría del Derecho'),
    ('Ordenamiento jurídico', 'Conjunto jerárquico y sistemático de normas de un Estado.',         'Kelsen',       'Teoría del Derecho'),
    ('Estado de Derecho',     'Principio por el que gobernantes y gobernados se someten a la ley.','Constitución', 'Constitucional'),
]

ASIGNACIONES = [
    ('Derecho Procesal',       'Jurisdicción',      'Función jurisdiccional del Estado.'),
    ('Derecho Penal',          'Jurisdicción',      'Jurisdicción penal.'),
    ('Derecho Administrativo', 'Jurisdicción',      'Jurisdicción contencioso-administrativa.'),
    ('Derecho Procesal',       'Competencia',       'Reglas de competencia procesal.'),
    ('Derecho Administrativo', 'Competencia',       'Competencia administrativa.'),
    ('Derecho Laboral',        'Competencia',       'Competencia de los tribunales laborales.'),
    ('Derecho Civil',          'Sujeto de derecho', 'Personas físicas y jurídicas.'),
    ('Derecho Constitucional', 'Sujeto de derecho', 'Titulares de derechos fundamentales.'),
    ('Derecho Civil',          'Obligación',        'Obligaciones civiles.'),
    ('Derecho Mercantil',      'Obligación',        'Obligaciones mercantiles.'),
    ('Derecho Laboral',        'Obligación',        'Obligaciones laborales.'),
]


def cargar(apps, schema_editor):
    Rama            = apps.get_model('myapp', 'Rama')
    Subrama         = apps.get_model('myapp', 'Subrama')
    Concepto        = apps.get_model('myapp', 'Concepto')
    SubramaConcepto = apps.get_model('myapp', 'SubramaConcepto')
    TerminoGeneral  = apps.get_model('myapp', 'TerminoGeneral')

    ramas_obj = {}
    for nombre, desc in RAMAS:
        r, _ = Rama.objects.get_or_create(nombre=nombre, defaults={'descripcion': desc})
        ramas_obj[nombre] = r

    sub_obj = {}
    for rama_nombre, subramas in SUBRAMAS.items():
        for s in subramas:
            obj, _ = Subrama.objects.get_or_create(
                rama=ramas_obj[rama_nombre], nombre=s,
            )
            sub_obj[s] = obj

    con_obj = {}
    for nombre, definicion, categoria in CONCEPTOS:
        c, _ = Concepto.objects.get_or_create(
            nombre=nombre,
            defaults={'definicion': definicion, 'categoria': categoria},
        )
        con_obj[nombre] = c

    for sub, con, nota in ASIGNACIONES:
        SubramaConcepto.objects.get_or_create(
            subrama=sub_obj[sub], concepto=con_obj[con],
            defaults={'nota': nota},
        )

    for termino, definicion, fuente, categoria in TERMINOS_GENERALES:
        TerminoGeneral.objects.get_or_create(
            termino=termino,
            defaults={'definicion': definicion, 'fuente': fuente, 'categoria': categoria},
        )


def descargar(apps, schema_editor):
    Rama           = apps.get_model('myapp', 'Rama')
    Concepto       = apps.get_model('myapp', 'Concepto')
    TerminoGeneral = apps.get_model('myapp', 'TerminoGeneral')
    Concepto.objects.all().delete()
    TerminoGeneral.objects.all().delete()
    Rama.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(cargar, descargar),
    ]
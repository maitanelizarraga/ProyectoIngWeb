from django.contrib import admin
from .models import (
    Rama, Subrama, Concepto, SubramaConcepto,
    TerminoGeneral, Sugerencia,
)


class SubramaInline(admin.TabularInline):
    model = Subrama
    extra = 1
    fields = ('nombre', 'descripcion')


class SubramaConceptoInline(admin.TabularInline):
    model = SubramaConcepto
    extra = 1
    autocomplete_fields = ['concepto']


@admin.register(Rama)
class RamaAdmin(admin.ModelAdmin):
    list_display  = ('nombre',)
    search_fields = ('nombre',)
    inlines       = [SubramaInline]


@admin.register(Subrama)
class SubramaAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'rama')
    list_filter   = ('rama',)
    search_fields = ('nombre',)
    autocomplete_fields = ['rama']
    inlines       = [SubramaConceptoInline]


@admin.register(Concepto)
class ConceptoAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'categoria')
    list_filter   = ('categoria',)
    search_fields = ('nombre', 'definicion')


@admin.register(SubramaConcepto)
class SubramaConceptoAdmin(admin.ModelAdmin):
    list_display = ('concepto', 'subrama', 'nota')
    list_filter  = ('subrama__rama', 'subrama')
    autocomplete_fields = ['subrama', 'concepto']


@admin.register(TerminoGeneral)
class TerminoGeneralAdmin(admin.ModelAdmin):
    list_display  = ('termino', 'categoria', 'fuente')
    list_filter   = ('categoria',)
    search_fields = ('termino', 'definicion')


@admin.register(Sugerencia)
class SugerenciaAdmin(admin.ModelAdmin):
    list_display    = ('nombre', 'email', 'fecha')
    readonly_fields = ('fecha',)
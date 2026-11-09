from django.db import models
from django.utils import timezone


# ============================================================
# RAMA
# ============================================================
class Rama(models.Model):
    """Rama principal del Derecho: Público o Privado."""

    nombre      = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Rama'
        verbose_name_plural = 'Ramas'

    def __str__(self):
        return self.nombre


# ============================================================
# SUBRAMA
# ============================================================
class Subrama(models.Model):
    """Subrama concreta: Derecho Administrativo, Civil, Penal, etc."""

    rama        = models.ForeignKey(
        Rama, on_delete=models.PROTECT, related_name='subramas'
    )
    nombre      = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['rama__nombre', 'nombre']
        constraints = [
            models.UniqueConstraint(
                fields=['rama', 'nombre'],
                name='uq_subrama_rama_nombre',
            )
        ]
        verbose_name = 'Subrama'
        verbose_name_plural = 'Subramas'

    def __str__(self):
        return f'{self.nombre} ({self.rama.nombre})'


# ============================================================
# CONCEPTO  (reutilizable entre subramas)
# ============================================================
class Concepto(models.Model):
    """Concepto jurídico que puede repetirse en varias subramas."""

    nombre      = models.CharField(max_length=150, unique=True)
    definicion  = models.TextField()
    categoria   = models.CharField(max_length=80, blank=True)
    subramas    = models.ManyToManyField(
        Subrama,
        through='SubramaConcepto',
        related_name='conceptos',
        blank=True,
    )
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Concepto'
        verbose_name_plural = 'Conceptos'

    def __str__(self):
        return self.nombre


# ============================================================
# SUBRAMA ↔ CONCEPTO  (tabla puente N:M)
# ============================================================
class SubramaConcepto(models.Model):
    """Asignación de un concepto a una subrama.
    Un mismo concepto puede existir en varias subramas,
    incluso de distinta rama (p. ej. 'Jurisdicción')."""

    subrama  = models.ForeignKey(
        Subrama, on_delete=models.CASCADE, related_name='conceptos_asignados'
    )
    concepto = models.ForeignKey(
        Concepto, on_delete=models.CASCADE, related_name='asignaciones'
    )
    nota     = models.TextField(
        blank=True,
        help_text='Cómo se aplica el concepto en esta subrama (opcional).',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['subrama', 'concepto'],
                name='uq_subrama_concepto',
            )
        ]
        ordering = ['subrama__nombre', 'concepto__nombre']
        verbose_name = 'Subrama–Concepto'
        verbose_name_plural = 'Subramas–Conceptos'

    def __str__(self):
        return f'{self.concepto.nombre} → {self.subrama.nombre}'


# ============================================================
# TÉRMINOS Y DEFINICIONES GENERALES (glosario)
# ============================================================
class TerminoGeneral(models.Model):
    """Glosario general e independiente de las ramas."""

    termino     = models.CharField(max_length=150, unique=True)
    definicion  = models.TextField()
    fuente      = models.CharField(max_length=200, blank=True)
    categoria   = models.CharField(max_length=80, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['termino']
        verbose_name = 'Término general'
        verbose_name_plural = 'Términos generales'

    def __str__(self):
        return self.termino


# ============================================================
# SUGERENCIAS  (feedback del usuario)
# ============================================================
class Sugerencia(models.Model):
    nombre  = models.CharField(max_length=100)
    email   = models.EmailField(blank=True)
    mensaje = models.TextField()
    fecha   = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Sugerencia'
        verbose_name_plural = 'Sugerencias'

    def __str__(self):
        return f'Sugerencia de {self.nombre} ({self.fecha:%Y-%m-%d})'
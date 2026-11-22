from django.forms import ModelForm
from .models import TerminoGeneral

class TerminoForm(ModelForm):
    class Meta:
        model = TerminoGeneral
        fields = ['termino', 'definicion', 'categoria', 'fuente']
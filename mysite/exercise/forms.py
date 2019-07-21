from django import forms
from django.utils.translation import ugettext_lazy as _

from exercise.models import UsuarioArgenitna

class UsuarioArgentinaForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    fecha_nacimiento = forms.DateField(
        label=_('Fecha nacimiento'),
        input_formats=('%d/%m/%Y', '%d-%m-%Y'), help_text=_('Formato: DD/MM/AAAA'),
        widget=forms.widgets.DateInput(format='%d/%m/%Y'),
        required=True
    )
    sexo = forms.ChoiceField(widget=forms.RadioSelect, choices=UsuarioArgenitna.SEXO_CHOICES)

    def __init__(self, *args, **kwargs):
        super(UsuarioArgentinaForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            if instance.validation_level==3:
                self.fields['tipo_documento'].disabled = True
                self.fields['numero_documento'].disabled = True
                self.fields['apellido'].disabled = True
                self.fields['nombre'].disabled = True
                self.fields['fecha_nacimiento'].disabled = True
                self.fields['sexo'].disabled = True

    class Meta:
        model = UsuarioArgenitna
        fields = [
            'tipo_documento',
            'numero_documento',
            'apellido',
            'nombre',
            'sexo',
            'fecha_nacimiento',
            'email',
            'password',
        ]

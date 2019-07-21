import random
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

CUIT_REGEX = r'^(20|23|24|27|30|33|34)-[0-9]{8}-[0-9]$'
NAMES_REGEX = r'^[a-zA-Z\s]+$'
NOT_UPDATE_ALLOW_FIELDS=[
    'tipo_documento',
    'numero_documento',
    'apellido',
    'nombre',
    'sexo',
    'validation_level'
]

def calculate_validation_level():
    return random.choice([0,3])


def changed_fields(new_instance, old_instance, exclude_fields=None):
    """Changed Fields
    Dada dos instancias de un mismo modelo retorna lo campos que se cambiaron.
    """
    ret = []
    if not exclude_fields:
        exclude_fields = []

    for field in new_instance._meta.get_fields():
        if field.name not in exclude_fields:
            if getattr(new_instance, field.name) != getattr(old_instance, field.name):
                ret.append(field.name)

    return ret

cuil_validator = RegexValidator(
    CUIT_REGEX,
    _('El cuit ingresado no tiene un formato válido')
)

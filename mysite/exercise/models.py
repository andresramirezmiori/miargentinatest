from datetime import date
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from exercise.helpers.models import (
    calculate_validation_level,
    CUIT_REGEX,
    NAMES_REGEX,
    changed_fields,
    NOT_UPDATE_ALLOW_FIELDS,
    cuil_validator
)

class UsuarioArgenitna(models.Model):
    """UsuarioArgentina.
    Representación de un usuario a registrar. Como es solo a nivel practico
    no tiene realcion con el usuario de Django, en otro caso la forma correcta
    es heredar del mismo
    """
    DNI = 'DNI'
    CUIL = 'CUIL'
    PAS = 'PAS'
    TIPO_DOCUMENTO_CHOICES = (
        (DNI, 'DNI'),
        (CUIL, 'CUIL'),
        (PAS, 'Pasaporte')
    )

    SEXO_MASCULINO = 'M'
    SEXO_FEMENINO = 'F'
    SEXO_CHOICES = (
        (SEXO_MASCULINO, 'Masculino'),
        (SEXO_FEMENINO, 'Femenino')
    )

    tipo_documento = models.CharField(_('tipo documento'), max_length=4, choices=TIPO_DOCUMENTO_CHOICES)
    # Se esta asumiendo que el pasaporte no tiene una longitud mayor que el CUIL
    numero_documento = models.CharField(
        _('número de documento'),
        help_text=_('Para CUIL usar formato ##-########-#'),
        max_length=13
    )
    nombre = models.CharField(
        _('nombre'),
        max_length=255,
        validators=[RegexValidator(NAMES_REGEX, _('El nombre solo permite letras y espacios'))]
    )
    apellido = models.CharField(
        _('apellido'),
        max_length=255,
        validators=[RegexValidator(NAMES_REGEX, _('El apellido solo permite letras y espacios'))]
    )
    sexo = models.CharField(_('sexo'), max_length=1, choices=SEXO_CHOICES)
    fecha_nacimiento = models.DateField(_('fecha nacimiento'))
    email = models.EmailField(_('correo electrónico'))
    password = models.CharField(_('contraseña'),
        max_length=100,
        validators=[MinLengthValidator(8,_('La contraseña debe contener al menos 8 caracteres'))])

    validation_level = models.PositiveIntegerField(
        _('nivel de validacion'),
        default= calculate_validation_level,
        blank=True,
    )

    def clean(self):
        super(UsuarioArgenitna, self).clean()
        # Validaction de tipo de documento cuando es CUIT
        if self.tipo_documento==self.CUIL:
            try:
                cuil_validator(self.numero_documento)
            except ValidationError as err:
                raise ValidationError({
                    'numero_documento': err.message
                })

        # Validacion fecha nacimiento anterior a hoy
        if not self.fecha_nacimiento:
            raise ValidationError({
                'fecha_nacimiento': _('La fecha de nacimiento tiene '
                    'un formato incorrecto o no ha sido completada')
            })

        if self.fecha_nacimiento > date.today():
            raise ValidationError({
                'fecha_nacimiento': _('La fecha de nacimiento tiene que ser anterior al día actual')
            })

        if self.pk:
            self._update_validations()

    def _update_validations(self):
        """ Update Validations
        Valida que no se realicen modificaiones no permitidas
        por nivel de validacion del usuario actual.
        """
        if self.validation_level == 3:
            # Solo se pude editar el mail o la contraseñas
            database_instance = self.__class__.objects.get(pk=self.pk)
            calculated_changed_fields = changed_fields(self, database_instance)
            # Si algun cambio cambiado es comun con algun campo no permitido => error
            if set(NOT_UPDATE_ALLOW_FIELDS) & set(calculated_changed_fields):
                raise ValidationError('Solo se puede modificar email y contraseña, para usuarios de nivel 3')

    def get_absolute_url(self):
        return reverse('user_detail', args=[str(self.pk)])

    def __str__(self):
        return f"{self.apellido} - {self.nombre}"

    class Meta:
        unique_together = ('tipo_documento', 'numero_documento')

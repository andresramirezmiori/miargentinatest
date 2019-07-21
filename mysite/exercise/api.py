from datetime import date
from rest_framework import serializers, viewsets
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _

from exercise.helpers.models import cuil_validator, changed_fields, NOT_UPDATE_ALLOW_FIELDS
from exercise.models import UsuarioArgenitna


class UsuarioArgenitnaSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'},
        validators=[MinLengthValidator(8,_('La contraseña debe contener al menos 8 caracteres'))]
    )

    def validate_fecha_nacimiento(self, value):
        if value > date.today():
            raise serializers.ValidationError(
                 _('La fecha de nacimiento tiene que ser anterior al día actual'))
        return value

    def validate(self, data):
        """
        Check CUIL regex.
        """
        if data['tipo_documento'] == UsuarioArgenitna.CUIL:
            try:
                cuil_validator(data['numero_documento'])
            except ValidationError as err:
                raise serializers.ValidationError({'numero_documento':err.message})
        return data

    def update(self, instance, validated_data):
        #validate changes before update then call super
        if instance and instance.validation_level==3:
            new_instance = UsuarioArgenitna(**validated_data)
            calculated_changed_fields = changed_fields(new_instance, instance, exclude_fields=['id', 'validation_level'])
            # Si algun cambio cambiado es comun con algun campo no permitido => error
            if set(NOT_UPDATE_ALLOW_FIELDS) & set(calculated_changed_fields):
                raise serializers.ValidationError(_('Solo se puede modificar email y contraseña, para usuarios de nivel 3'))
            return super(UsuarioArgenitnaSerializer, self).update(instance, validated_data)


    class Meta:
        model = UsuarioArgenitna
        fields = (
            'url',
            'tipo_documento',
            'numero_documento',
            'apellido',
            'nombre',
            'sexo',
            'fecha_nacimiento',
            'email',
            'password',
            'validation_level',
        )
        read_only_fields = ('validation_level',)


class UsuarioArgenitnaViewSet(viewsets.ModelViewSet):
    queryset = UsuarioArgenitna.objects.all()
    serializer_class = UsuarioArgenitnaSerializer

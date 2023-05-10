from django.db import models
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class CartMixin(models.Model):
    product = models.PositiveBigIntegerField(verbose_name=_('Номер типа сущности'))

    class Meta:
        abstract = True


class CartSerializerMixin(serializers.Serializer):
    pass

from django.db import models
from rest_framework import serializers


class CartMixin(models.Model):
    product = models.PositiveBigIntegerField(verbose_name='Номер типа сущности')

    class Meta:
        abstract = True


class CartSerializerMixin(serializers.Serializer):
    pass
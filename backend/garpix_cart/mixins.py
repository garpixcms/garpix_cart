from django.db import models


class CartMixin(models.Model):
    product = models.PositiveBigIntegerField(verbose_name='Номер типа сущности')

    class Meta:
        abstract = True

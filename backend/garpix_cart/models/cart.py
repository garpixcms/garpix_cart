from django.conf import settings
from django.db import models
from django.utils.module_loading import import_string

CartMixin = import_string(settings.GARPIX_CART_MIXIN)


class CartItem(CartMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    params = models.JSONField(blank=True, null=True, default=dict, verbose_name='Дополнительные параметры')
    count = models.PositiveIntegerField(default=1, verbose_name='Количество')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'{self.pk}'

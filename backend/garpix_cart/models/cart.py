from django.db import models
from django.utils.module_loading import import_string
from garpix_user.models import UserSession
from django.conf import settings
from django.utils.translation import gettext_lazy as _

CartMixin = import_string(settings.GARPIX_CART_MIXIN)


class CartItem(CartMixin):
    customer = models.ForeignKey(UserSession, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    params = models.JSONField(blank=True, null=True, default=dict, verbose_name=_('Дополнительные параметры'))
    count = models.PositiveIntegerField(default=1, verbose_name=_('Количество'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Создано'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Обновлено'))

    @property
    def user(self):
        return self.customer.user

    class Meta:
        verbose_name = _('Корзина')
        verbose_name_plural = _('Корзины')

    def __str__(self):
        return f'{self.pk}'

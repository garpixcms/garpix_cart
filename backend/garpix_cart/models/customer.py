from django.db import models
from django.conf import settings
from django.utils import timezone


class Customer(models.Model):
    class CustomerState(models.IntegerChoices):
        UNRECOGNIZED = 0, 'Неопознанный'
        GUEST = 1, 'Гость'
        REGISTERED = 2, 'Зарегистрированный'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    number = models.CharField(max_length=256, null=True, blank=True, verbose_name='id customer')
    recognized = models.PositiveIntegerField(
        default=CustomerState.UNRECOGNIZED,
        choices=CustomerState.choices,
        verbose_name='Тип',
        help_text='Обозначает состояние, в котором распознается заказчик.'
    )
    last_access = models.DateTimeField(
        'Последний вход',
        default=timezone.now,
    )

    @classmethod
    def get_from_request(cls, request):
        user = request.user
        if user.is_authenticated:
            return Customer.objects.filter(user=user).first()

        token = request.headers.get('Cart-Token', None)
        if token is not None:
            return Customer.objects.filter(number=token).first()

        token = request.session.session_key
        if token is not None:
            return Customer.objects.filter(number=token).first()
        return None

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.pk}'
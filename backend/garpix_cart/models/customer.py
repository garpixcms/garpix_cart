import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model


class Customer(models.Model):
    class CustomerState(models.IntegerChoices):
        UNRECOGNIZED = (0, 'Неопознанный')
        GUEST = (1, 'Гость')
        REGISTERED = (2, 'Зарегистрированный')

    user = models.OneToOneField(
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

    @classmethod
    def set_user_from_request(cls, request):
        customer = cls.get_from_request(request)
        if request.user.is_authenticated and customer is not None:
            user = get_user_model().objects.get(pk=request.user.pk)
            customer.user = user
            customer.save()
            return True
        return False

    @classmethod
    def get_or_create_customer(cls, request, session=False):
        customer = cls.get_from_request(request)
        if customer is not None:
            return customer

        if request.user.is_authenticated:
            user = get_user_model().objects.get(pk=request.user.pk)
            return Customer.objects.create(
                user=user,
                recognized=Customer.CustomerState.REGISTERED
            )

        if session is True:
            token = request.session.session_key
            return Customer.objects.create(
                number=token,
                recognized=Customer.CustomerState.GUEST
            )

        return Customer.objects.create(
            number=uuid.uuid4(),
            recognized=Customer.CustomerState.GUEST
        )

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.pk}'

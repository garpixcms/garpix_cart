import uuid
from typing import Optional

from django.conf import settings
from django.utils.module_loading import import_string
from django.contrib.auth import get_user_model

from rest_framework import parsers
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from ..models import CartItem, Customer
from ..permissions import IsCustomer
from ..serializers import CartItemSerializer, CustomerSerializer


class CartView(viewsets.ViewSet):
    parser_classes = (parsers.JSONParser,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_customer(self) -> Optional[Customer]:
        return Customer.get_from_request(self.request)

    def get_or_create_customer(self, session=False):
        # TODO перенести в модель
        customer = self.get_customer()
        if customer is not None:
            return customer

        if self.request.user.is_authenticated:
            user = get_user_model().objects.get(pk=self.request.user.pk)
            return Customer.objects.create(
                user=user,
                recognized=Customer.CustomerState.REGISTERED
            )

        if session is True:
            token = self.request.session.session_key
            return Customer.objects.create(
                number=token,
                recognized=Customer.CustomerState.GUEST
            )

        return Customer.objects.create(
            number=uuid.uuid4(),
            recognized=Customer.CustomerState.GUEST
        )

    def get_cartitems(self):
        customer = self.get_customer()
        CartItem.objects.filter(customer=customer)

    def create_cart_items(self, customer, data):
        elements = []
        for item in data:
            elements.append(CartItem(
                customer=customer,
                **item
            ))

        CartItem.objects.bulk_create(elements)

    def remove_cart_items(self, data):
        customer = self.get_customer()
        print(customer, 'customer remove_cart_items')
        CartItem.objects.filter(customer=customer, pk__in=data).delete()

    def list(self, request):
        return Response(CartItemSerializer(self.get_cartitems(), many=True).data)

    @action(detail=False, methods=['GET'], permission_classes=(permissions.AllowAny,))
    def create_customer(self, request):
        return Response({
            'customer': CustomerSerializer(self.get_or_create_customer()).data
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'data': openapi.Schema(
                    type=openapi.TYPE_ARRAY, description='Массив с данными',
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'product': openapi.Schema(
                                type=openapi.TYPE_INTEGER, description='ID продукта',
                            ),
                            'count': openapi.Schema(
                                type=openapi.TYPE_INTEGER, description='Количество',
                            ),
                            'params': openapi.Schema(
                                type=openapi.TYPE_OBJECT, description='Дополнительные параметры',
                            )
                        }
                    )
                )
            }
        )
    )
    @action(detail=False, methods=['POST'], permission_classes=(IsCustomer,))
    def add(self, request):
        customer = self.get_customer()
        data = request.data.get('data', None)

        if data is not None:
            self.create_cart_items(customer=customer, data=data)

            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)

        return Response(
            {'server': 'Request "data" must be dict.'}, status=status.HTTP_400_BAD_REQUEST
        )

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'data': openapi.Schema(
                    description='ID корзины',
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER)
                )
            }
        )
    )
    @action(detail=False, methods=['DELETE'], permission_classes=(IsCustomer,))
    def remove(self, request):
        data = request.data.get('data')
        self.remove_cart_items(data)
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], permission_classes=(permissions.AllowAny,))
    def session_list(self, request):
        return Response(
            self.get_cartitems(), status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['DELETE'], permission_classes=(IsCustomer,))
    def session_remove(self, request):
        data = request.data.get('data')
        self.remove_cart_items(data)
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'], permission_classes=(permissions.AllowAny,))
    def session_add(self, request):
        customer = self.get_or_create_customer(session=True)
        data = request.data.get('data', None)

        if data is not None:
            self.create_cart_items(customer=customer, data=data)

            return Response(
                {'server': 'Product added successfully.'}, status=status.HTTP_200_OK
            )

        return Response(
            {'error': 'Data not valid'}, status=status.HTTP_400_BAD_REQUEST
        )

    def partial_update(self, request, pk=None):
        customer = self.get_customer()

        cart_item = CartItem.objects.filter(customer=customer, pk=pk)

        if cart_item.count() == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data.get('data')

        cart_item.update(**data)

        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)

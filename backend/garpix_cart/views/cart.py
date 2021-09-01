from django.conf import settings
from django.utils.module_loading import import_string

from rest_framework import parsers
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from ..models import CartItem
from ..serializers import CartItemSerializer

CartSession = import_string(settings.GARPIX_CART_SESSION_CLASS)


class CartView(viewsets.ViewSet):
    parser_classes = (parsers.JSONParser,)
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)
        return Response(CartItemSerializer(cart_items, many=True).data)

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
    @action(detail=False, methods=['post'])
    def add(self, request):
        user = request.user

        if request.data is not None and isinstance(request.data, dict):
            if data := request.data.get('data', None):
                elements = []
                for item in data:
                    elements.append(CartItem(
                        user=user,
                        **item
                    ))

                CartItem.objects.bulk_create(elements)

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
    @action(detail=False, methods=['delete'])
    def remove(self, request):
        user = request.user

        data = request.data.get('data')

        CartItem.objects.filter(user=user, pk__in=data).delete()

        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], permission_classes=(permissions.AllowAny,))
    def session_list(self, request):
        base_cart_session = CartSession(request.session)

        return Response(
            base_cart_session.list(), status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['POST'], permission_classes=(permissions.AllowAny,))
    def session_remove(self, request):
        data = request.data.get('data', None)
        base_cart_session = CartSession(request.session)

        if base_cart_session.remove.is_valid(data):
            base_cart_session.remove.make(data)

            return Response(
                {'server': 'Product removed successfully.'}, status=status.HTTP_200_OK
            )

        return Response(
            {'server': base_cart_session.remove.error_log(data)}, status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['POST'], permission_classes=(permissions.AllowAny,))
    def session_add(self, request):
        """
        {
            "data":
            [
                {
                    "product": "1",
                    "params": "data",
                    "count": "1"
                }
            ]
        }
        """

        data = request.data.get('data', None)
        base_cart_session = CartSession(request.session)

        if base_cart_session.add.is_valid(data):
            base_cart_session.add.make(data)

            return Response(
                {'server': 'Product added successfully.'}, status=status.HTTP_200_OK
            )

        return Response(
            {'server': base_cart_session.add.error_log(data)}, status=status.HTTP_400_BAD_REQUEST
        )

    def partial_update(self, request, pk=None):
        user = request.user

        cart_item = CartItem.objects.filter(user=user, pk=pk)

        if cart_item.count() == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data.get('data')

        cart_item.update(**data)

        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)

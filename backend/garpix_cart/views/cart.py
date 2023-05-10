from typing import Optional

from drf_spectacular.utils import extend_schema
from garpix_user.models import UserSession
from garpix_user.utils.drf_spectacular import user_session_token_header_parameter
from rest_framework import parsers
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import CartItem
from ..permissions import IsCustomer
from ..serializers import CartItemSerializer, CartItemListSerializer


@extend_schema(
    parameters=[
        user_session_token_header_parameter()
    ]
)
class CartView(viewsets.ViewSet):
    parser_classes = (parsers.JSONParser,)
    permission_classes = (permissions.AllowAny,)
    serializer_classes = {
        'add': CartItemListSerializer,
        'session_add': CartItemListSerializer
    }

    default_serializer_class = CartItemSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_customer(self) -> Optional[UserSession]:
        return UserSession.get_from_request(self.request)

    def get_or_create_customer(self, session=False):
        return UserSession.get_or_create_user_session(request=self.request, session=session)

    def get_cartitems(self):
        customer = self.get_customer()
        return CartItem.objects.filter(customer=customer)

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
        CartItem.objects.filter(customer=customer, pk__in=data).delete()

    def list(self, request):
        return Response(CartItemSerializer(self.get_cartitems(), many=True).data)

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

from django.utils.module_loading import import_string
from rest_framework.serializers import ModelSerializer, Serializer
from django.conf import settings
from ..models import CartItem


CartItemMixin = import_string(settings.GARPIX_CART_SERIALIZER_MIXIN)


class CartItemSerializer(ModelSerializer, CartItemMixin):
    class Meta:
        model = CartItem
        fields = (
            '__all__'
        )


class CartItemListSerializer(Serializer):
    data = CartItemSerializer(many=True, required=True)

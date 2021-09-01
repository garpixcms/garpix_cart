from rest_framework.routers import DefaultRouter

from .views import CartView

router = DefaultRouter()

router.register(r'cart_items', CartView, basename='cart-items')

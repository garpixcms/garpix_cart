from rest_framework.routers import DefaultRouter

from .views import CartView

router = DefaultRouter()

router.register(r'cart', CartView, basename='cart')

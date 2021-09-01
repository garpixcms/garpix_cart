from django.conf import settings
from django.utils import timezone
from django.utils.module_loading import import_string

from ..exceptions import CartError
from ..utils import make_session_format

CartHandler = import_string(settings.GARPIX_CART_SESSION_HANDLER_CLASS)


class BaseCartAdd(CartHandler):
    def make(self, products):
        cart = self._core.get()
        formatted_products = make_session_format(products)
        updates = [num for num, items in enumerate(formatted_products.items()) if items[0] in cart]

        for num, product in enumerate(products):
            if num not in updates:
                product['created_at'] = timezone.now().strftime("%m.%d.%Y, %H:%M:%S")
            else:
                del products[num]
                product = cart.get(product['product'])

            product['updated_at'] = timezone.now().strftime("%m.%d.%Y, %H:%M:%S")

        cart.update(make_session_format(products))
        return self._core.modify_session(cart)


class BaseCartRemove(CartHandler):
    def validate(self, products):
        cart = self._core.get()
        formatted_products = make_session_format(products)

        for key, _ in formatted_products.items():
            if key not in cart:
                raise CartError(f'Key {key} does not exist')
        return super().validate(products)

    def make(self, products):
        cart = self._core.get()

        products = make_session_format(products)

        for key, _ in products.items():
            del cart[key]

        return self._core.modify_session(cart)


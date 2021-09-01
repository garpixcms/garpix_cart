from garpixcms.settings import *  # noqa

INSTALLED_APPS += [
    'garpix_cart',
]

GARPIX_CART_SESSION_KEY = 'cart'

GARPIX_CART_MIXIN = 'garpix_cart.mixins.CartMixin'
GARPIX_CART_SESSION_CLASS = 'garpix_cart.base.BaseCartSession'
GARPIX_CART_SESSION_HANDLER_CLASS = 'garpix_cart.base.BaseCartHandler'

from garpixcms.settings import *  # noqa

INSTALLED_APPS += [
    'garpix_cart',
]

GARPIX_CART_SESSION_KEY = 'cart'

GARPIX_CART_MIXIN = 'garpix_cart.mixins.CartMixin'

MIGRATION_MODULES.update({
    'garpix_cart': 'app.migrations.garpix_cart',
})

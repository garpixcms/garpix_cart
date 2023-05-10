from garpixcms.settings import *  # noqa
from garpix_user.settings import *  # noqa

INSTALLED_APPS += [
    'garpix_cart'
]

MIGRATION_MODULES.update({
    'garpix_cart': 'app.migrations.garpix_cart'
})

GARPIX_USER = {

}


GARPIX_CART_SESSION_KEY = 'cart'

GARPIX_CART_MIXIN = 'garpix_cart.mixins.CartMixin'
GARPIX_CART_SERIALIZER_MIXIN = 'garpix_cart.mixins.CartSerializerMixin'

SPECTACULAR_SETTINGS = {
    'TITLE': 'Garpix cart API',
    'DESCRIPTION': '',
    'VERSION': '3.0.0',
}

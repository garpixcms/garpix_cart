from logging import getLogger

from django.utils.translation import gettext as _

from ..abstracts import AbstractCartHandler
from ..exceptions import CartError

logger = getLogger(__name__)


class BaseCartHandler(AbstractCartHandler):
    def __init__(self, core):
        self._core = core

    def make(self, products):
        pass

    def validate(self, products):
        if isinstance(products, list):
            return products
        raise CartError(
            _('"products" must be list.')
        )

    def is_valid(self, products):
        try:
            self.validate(products)
        except CartError:
            return False
        return True

    def error_log(self, products):
        try:
            self.validate(products)
        except CartError as error:
            logger.debug(
                str(error)
            )
            return str(error)
        return None

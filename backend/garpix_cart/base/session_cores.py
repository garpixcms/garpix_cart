from django.conf import settings

from ..base.session_handlers import BaseCartAdd, BaseCartRemove
from ..abstracts import AbstractCartSession

CART_SESSION_KEY = settings.GARPIX_CART_SESSION_KEY


class BaseCartSession(AbstractCartSession):
    def __init__(self, session):
        self.__session = session
        self.add = BaseCartAdd(self)
        self.remove = BaseCartRemove(self)

    def get(self):
        return self.__session.get(CART_SESSION_KEY, {})

    def list(self):
        return [self.get()]

    def modify_session(self, values):
        self.__session[CART_SESSION_KEY] = values

        return True

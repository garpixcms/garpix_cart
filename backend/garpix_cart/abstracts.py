from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List


class AbstractCartSession(ABC):
    @abstractmethod
    def get(self) -> Optional[Dict[str, Any]]:
        # get session from request

        ...

    @abstractmethod
    def modify_session(self, values) -> bool:
        # modify session from request

        ...


class AbstractCartHandler(ABC):
    @abstractmethod
    def validate(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # validate data from request.data

        ...

    @abstractmethod
    def is_valid(self, products: List[Dict[str, Any]]) -> bool:
        # check data is valid

        ...

    @abstractmethod
    def make(self, products: List[Dict[str, Any]]) -> bool:
        # make if data is valid
        # always returns modify_session() from CartSession class

        ...

    @abstractmethod
    def error_log(self, products: List[Dict[str, Any]]) -> Optional[str]:
        # get errors if they raised

        ...

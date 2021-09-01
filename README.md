# Garpix Cart


User Cart module for Django/DRF projects. Part of GarpixCMS.

## Quickstart

Install with pip 

    $ pip install garpix_cart

Add the `garpix_cart` to your INSTALLED_APPS:

```python
# settings.py

INSTALLED_APPS = [
    # ...
    'garpix_cart',
]
```

Make migrations and migrate database:

    $ ./manage.py makemigrations
    $ ./manage.py migrate

Add to `urls.py`:

```
urlpatterns = [
    # ...
    path('', include('garpix_cart.urls'))
]
```

### Customize

By default, you will see in `settings.py`:

```
GARPIX_CART_SESSION_KEY = 'cart' # cart session key 

GARPIX_CART_MIXIN = 'garpix_cart.mixins.CartMixin' # base Cart mixin to model
GARPIX_CART_SESSION_CLASS = 'garpix_cart.base.BaseCartSession' # base cart session core
GARPIX_CART_SESSION_HANDLER_CLASS = 'garpix_cart.base.BaseCartHandler' # base cart handler, which inherit all handlers
```

#### Easy way to customize

For example, we want to have our own BaseCartHandler:

1) override as needed;

```
# base.py

from garpix_cart.base import BaseCartHandler


class CustomHandler(BaseCartHandler):
    def validate(self, products) -> List[Dict[str, Any]]:
        return products
```

Where `products` is received data from request

2) Change handler in `settings.py`;

```
# settings.py

GARPIX_CART_SESSION_HANDLER_CLASS = 'app.base.CustomHandler'
```

3) This work fine!


#### The hard way to customize

1) Create your class inherited from abstract;

```
# base.py

from garpix_cart.abstracts import AbstractCartHandler


class CustomHandler(AbstractCartHandler):
    def validate(self, products) -> List[Dict[str, Any]]:
        # method validates the data from the request
        
        ...

    def is_valid(self, products) -> bool:
        # check data is valid

        ...
    
    def make(self, products) -> bool:
        # make if data is valid
        # always returns modify_session() from CartSession class
    
        ...

    def error_log(self, products) -> Optional[str]:
        # get errors if they raises
    
        ...
``` 

2) Change handler in `settings.py`;

```
# settings.py

GARPIX_CART_SESSION_HANDLER_CLASS = 'app.base.CustomHandler'
```

3) This work fine!


Developed by Garpix / [https://garpix.com](https://garpix.com)
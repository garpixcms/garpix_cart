# Garpix Cart

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

and to migration modules:

```python
# settings.py

# ...
MIGRATION_MODULES = {
    'garpix_cart': 'app.migrations.garpix_cart',
}
```

Make migrations and migrate database:

    $ ./manage.py makemigrations
    $ ./manage.py migrate

Add to `urls.py`:

```
urlpatterns = [
    # ...
    # garpix_cart
    path('', include(('garpix_cart.urls', 'cart'), namespace='garpix_cart')),
]
```

В интернет магазине обычно посетитель начинает искать интересные товары, надеясь добавить несколько из них в свою корзину. 
Затем по пути к оформлению заказа они решают, создать ли учетную запись пользователя, использовать существующую или продолжить работу в качестве гостя. 
Здесь все усложняется.

Во-первых, для неаутентифицированных посетителей сайта корзина никому не принадлежит. Но каждая корзина должна быть 
связана с ее текущим посетителем сайта.

Во-вторых, когда корзина преобразована в заказ, но посетитель хочет продолжить работу в качестве гостя, этот объект заказа 
должен ссылаться на объект пользователя в базе данных. 
Такие пользователи будут рассматриваться как фальшивые: не могут войти в систему, сбросить пароль и т.д. 
Единственная информация, которую необходимо сохранить для такого фальшивого пользователя это их адрес электронной почты, 
иначе они не смогут быть проинформированы, когда бы ни состояние их порядок меняется.

Django явно не разрешает использование таких пользовательских объектов в своих моделях баз данных. 
Но, используя логический флаг is_active, мы можем обмануть приложение, чтобы оно интерпретировало такого гостя как 
фальшивого анонимного пользователя.

Такой подход неприменим для всех приложений на основе Django, добавляется новая модель - **Customer**


## setting.py

`GARPIX_CART_SERIALIZER_MIXIN` - можно задать миксин для сериалайзера элемента корзины

`GARPIX_CART_MIXIN` - можно задать миксин для модели элемента корзины


# Changelog

See [CHANGELOG.md](CHANGELOG.md).

# Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

# License

[MIT](LICENSE)

---

Developed by Garpix / [https://garpix.com](https://garpix.com)


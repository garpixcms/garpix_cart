def make_session_format(products):
    kwargs = {}

    for product in products:
        kwargs[product['product']] = product

    return kwargs

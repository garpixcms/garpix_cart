from garpixcms.urls import *  # noqa

urlpatterns = [path('api/v1/', include('garpix_cart.urls'))] + urlpatterns

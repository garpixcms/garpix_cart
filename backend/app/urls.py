from django.urls import path, re_path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf import settings


urlpatterns = []

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^api/v1/docs/schema/$', SpectacularAPIView.as_view(), name='schema'),
        re_path(r'^api/v1/docs/$', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        re_path(r'^api/v1/redoc/$', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]

urlpatterns += [path('api/v1/', include('garpix_cart.urls'))]

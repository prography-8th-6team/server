"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import SimpleRouter

from applications.billings.views import BillingViewSet, get_currencies
from applications.travels.views import TravelViewSet
from applications.users.views import UserViewSet, jwt_refresh_token

schema_view = get_schema_view(
    openapi.Info(
        title="JERNYLIST",
        default_version='v1',
        description=
        """
        JERNYLIST API 문서 페이지입니다.
        """,
    ),
    validators=['flex'],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = SimpleRouter(trailing_slash=False)

router.register('v1/users', UserViewSet, 'users')
router.register('v1/travels', TravelViewSet, 'travels')
router.register('v1/billings', BillingViewSet, 'billings')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),

    path('v1/currencies', get_currencies),
    path('v1/refresh_token', jwt_refresh_token),
]

if settings.DEBUG:
    urlpatterns += [
       re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
       re_path(r'^swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
       re_path(r'^redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]

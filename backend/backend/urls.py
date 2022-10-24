"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from django.conf.urls.static import static
from django.conf import settings
from .views import MyTokenObtainPairView
from django.views.generic import TemplateView
from rest_framework import permissions
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


router = routers.DefaultRouter()

schema_view = get_schema_view(
    openapi.Info(
        title="Smart Museum API",
        default_version='v1',
        description="Smart Museum Site Description",
        terms_of_service="https://smartseas.kr/",
        contact=openapi.Contact(email="locs.manage@gmail.com")
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

index = TemplateView.as_view(template_name='index.html')

urlpatterns = [
    # REACT APP
    path('', index),
    path('login', index),
    path('join', index),
    path('mypage', index),

    path('dashboard', index),
    path('exhibition', index),
    path('exhibition-add', index),
    path('exhibition-modify', index),
    path('inner-exhibition', index),
    path('inner-exhibition/', index),
    path('inner-exhibition-detail', index),
    path('inner-exhibition-add', index),
    path('inner-exhibition-modify', index),
    path('event', index),
    path('event-add', index),
    path('event-detail', index),
    path('event-modify', index),
    path('event-mission-add', index),
    path('event-mission-detail', index),
    path('event-mission-modify', index),

    path('service', index),
    path('service-select', index),
    path('system', index),
    path('system-user', index),
]

urlpatterns += [
    # Django Admin Page
    path('django_admin/', admin.site.urls),

    # JWT Token API
    path('api/v1/token-auth/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # REST API
    path('api/v1/account/', include('account.urls')),
    path('api/v1/museum/', include('museum.urls')),
    path('api/v1/event/', include('event.urls')),
    path('api/v1/beacon/', include('beacon.urls')),
    path('api/v1/history/', include('history.urls')),
]
urlpatterns += [
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    *static(settings.MEDIA_URL_1, document_root=settings.MEDIA_ROOT_1)
]


urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
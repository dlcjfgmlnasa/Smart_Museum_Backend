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
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from django.conf.urls.static import static
from django.conf import settings
from .views import MyTokenObtainPairView
from django.views.generic import TemplateView


urlpatterns = [
    # REACT APP
    # re_path('.*', TemplateView.as_view(template_name='index.html')),

    # JWT Token API
    path('api/v1/token-auth/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # REST API
    path('api/v1/account/', include('account.urls')),
    path('api/v1/musuem/', include('museum.urls')),
    path('api/v1/event/', include('event.urls'))
]
urlpatterns += [
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]


# -*- coding:utf-8 -*-
from django.urls import path
from . import views


urlpatterns = [
    path('',
         views.BeaconAPIView.as_view(),
         name='beacon get/put/delete'),
    path('<int:inner_exhibition_pk>/',
         views.BeaconAPIView2.as_view(),
         name='beacon post')
]

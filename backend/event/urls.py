# -*- coding:utf-8 -*-
from django.urls import path
from . import views


urlpatterns = [
    path('inner_exhibition/<int:inner_exhibition_pk>/',
         views.EventAPIView.as_view(),
         name='event create/read list'),
    path('<int:pk>/',
         views.EventDetailAPIView.as_view(),
         name='event read/update/delete'),
]

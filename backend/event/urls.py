# -*- coding:utf-8 -*-
from django.urls import path
from . import views


urlpatterns = [
    path('',
         views.EventAPIView.as_view(),
         name='normal event list/create'),
    path('list/',
         views.EventListAPIView.as_view(),
         name='normal event'),
    path('<int:pk>/',
         views.EventDetailAPIView.as_view(),
         name='event read/update/delete'),
    path('mission/<int:inner_exhibition_pk>/',
         views.EventMissionAPIView.as_view(),
         name='event inner_exhibition create/read list'),
    path('mission/',
         views.EventMissionListView.as_view(),
         name='event mission')
]

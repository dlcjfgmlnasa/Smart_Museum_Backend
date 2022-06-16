# -*- coding:utf-8 -*-
from django.urls import path
from . import views

urlpatterns = [
    path('',
         views.AccountView.as_view(),
         name='account'),
    path('<int:pk>/',
         views.AccountDetailView.as_view(),
         name='account create/update/delete'),
    path('list/',
         views.AccountListView.as_view(),
         name='account list')
]
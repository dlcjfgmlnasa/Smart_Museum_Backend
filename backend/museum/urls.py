# -*- coding:utf-8 -*-
from django.urls import path
from .views import *

# exhibition
urlpatterns = [
    path('<int:user_pk>/',
         ExhibitionAPIView.as_view(),
         name='exhibition - creat/read (based user_pk)'),
    path('exhibition/<int:pk>/',
         ExhibitionDetailAPIView.as_view(),
         name='exhibition - read/edit/delete (based pk)'
    ),
    path('exhibition/<int:exhibition_pk>/inner_exhibition/',
         InnerExhibitionAPIView.as_view(),
         name='inner exhibition - create (based exhibition_pk)'),
    path('inner_exhibition/<int:pk>/',
         InnerExhibitionDetailAPIView.as_view(),
         name='inner exhibition - read/edit/delete (based pk)')
]

# -*- coding:utf-8 -*-
from django.urls import path
from . import views


urlpatterns = [
    path('exhibition/<int:exhibition_pk>/day/',
         views.ExhibitionDayAPIView.as_view(),
         name='exhibition today'),
    path('exhibition/<int:exhibition_pk>/popularity/',
         views.ExhibitionPopularityAPIView.as_view(),
         name='exhibition popularity'),
    path('exhibition/<int:exhibition_pk>/time/',
         views.ExhibitionTimeAPIView.as_view(),
         name='exhibition time'),
    path('exhibition/<int:exhibition_pk>/foot_print/',
         views.ExhibitionFootPrintAPIView.as_view(),
         name='exhibition foot print'),
    path('inner_exhibition/<int:inner_exhibition_pk>/day/',
         views.InnerExhibitionDayAPIView.as_view(),
         name='inner_exhibition today'),
    path('inner_exhibition/<int:inner_exhibition_pk>/time/',
         views.InnerExhibitionTimeAPIView.as_view(),
         name='inner_exhibition time')
]

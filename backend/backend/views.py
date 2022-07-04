# -*- coding:utf-8 -*-
import os
from django.conf import settings
from django.views.generic import View
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

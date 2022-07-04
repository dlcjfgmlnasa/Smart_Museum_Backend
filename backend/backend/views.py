# -*- coding:utf-8 -*-
import os
from django.conf import settings
from django.views.generic import View
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ReactAppView(View):
    def get(self, request):
        print(request)
        print(os.path.abspath('.'))
        try:
            with open(os.path.join(str(settings.ROOT_DIR), 'Smart_Museum_Frontend', 'build', 'index.html'),
                      encoding='utf-8') as file:
                file = file.read()
                return HttpResponse(file)
        except FileNotFoundError:
            return HttpResponse(
                """
                index.html not found ! build your react app!!
                """,
                status=501,
            )
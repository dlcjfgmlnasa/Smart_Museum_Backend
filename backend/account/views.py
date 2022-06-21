# -*- coding:utf-8 -*-
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializer import AccountCreateSerializer, AccountSerializer
from .models import User


class AccountView(APIView):
    permission_classes = [AllowAny]

    # 회원 가입
    def post(self, request):
        serializer_cls = AccountCreateSerializer(data=request.data)
        if serializer_cls.is_valid():
            serializer_cls.save()

            return Response(
                serializer_cls.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer_cls.errors,
            status=status.HTTP_404_NOT_FOUND
        )


class AccountDetailView(APIView):
    @staticmethod
    def get_account(pk: int):
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, pk: int):
        model = self.get_account(pk=pk)

        if model is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer_cls = AccountSerializer(model)
        return Response(serializer_cls.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        model = self.get_account(pk=pk)

        if model is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer_cls = AccountSerializer(model, data=request.data)
        if serializer_cls.is_valid():
            serializer_cls.save()
            return Response(
                serializer_cls.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer_cls.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        model = self.get_account(pk=pk)

        if model is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AccountListView(APIView):
    def get(self, request):
        users = User.objects.filter(is_superuser=False)
        if users.count() != 0:
            serializer_cls = AccountSerializer(users, many=True)
            return Response(serializer_cls.data)
        return Response(
            {}, status=status.HTTP_200_OK
        )

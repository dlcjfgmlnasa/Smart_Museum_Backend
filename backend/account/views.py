# -*- coding:utf-8 -*-
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializer import AccountCreateSerializer, AccountSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from .models import User
from django.db.models import Q


class AccountSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


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


class AccountListView(ListAPIView):
    pagination_class = AccountSetPagination
    serializer_class = AccountSerializer

    def get_queryset(self):
        queryset = User.objects.filter()
        queryset = self.filter_queryset(queryset)
        return queryset

    def filter_queryset(self, queryset):
        username = self.request.GET.get('username')
        museum_name = self.request.GET.get('museum_name')
        museum_location = self.request.GET.get('museum_location')
        payment_state = self.request.GET.get('payment_state')
        service_plan = self.request.GET.get('service_plan')

        query = (username or museum_name or museum_location or payment_state or service_plan)
        if query:
            query_object = Q()
            if username:
                query_object.add(Q(username=username), Q.OR)
            if museum_name:
                query_object.add(Q(museum_name=museum_name), Q.OR)
            if museum_location:
                query_object.add(Q(museum_location=museum_location), Q.OR)
            if payment_state:
                query_object.add(Q(payment_state=payment_state), Q.OR)
            if service_plan:
                query_object.add(Q(service_plan=service_plan), Q.OR)
            queryset = queryset.filter(query_object)

        return queryset


class AccountList2View(APIView):
    def get(self, request):
        users = User.objects.all()
        if users.count() == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer_cls = AccountSerializer(users, many=True)
        return Response(
            serializer_cls.data,
            status=status.HTTP_200_OK
        )
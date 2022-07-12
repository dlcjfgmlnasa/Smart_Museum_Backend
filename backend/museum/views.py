# -*- coding:utf-8 -*-
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q


class ExhibitionSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 1000


class InnerExhibitionSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ExhibitionAPIView(APIView):
    @staticmethod
    def get_user(pk: int):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, user_pk: int):
        user = self.get_user(pk=user_pk)
        if user is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        exhibitions = user.exhibition.all()
        serializer_cls = ExhibitionSerializer(exhibitions, many=True)
        return Response(
            serializer_cls.data,
            status=status.HTTP_200_OK
        )

    def post(self, request, user_pk: int):
        user = self.get_user(pk=user_pk)
        if user is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        serializer_cls = ExhibitionSerializer(data=request.data)
        if serializer_cls.is_valid():
            serializer_cls.save(user=user)

            return Response(
                serializer_cls.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer_cls.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ExhibitionDetailAPIView(APIView):
    @staticmethod
    def get_exhibition(pk: int):
        try:
            return Exhibition.objects.get(id=pk)
        except Exhibition.DoesNotExist:
            return None

    def get(self, request, pk: int):
        exhibition = self.get_exhibition(pk=pk)
        if exhibition is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        serializer_cls = ExhibitionSerializer(exhibition)
        return Response(
            serializer_cls.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk: int):
        exhibition = self.get_exhibition(pk=pk)
        if exhibition is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        serializer_cls = ExhibitionSerializer(exhibition, data=request.data)
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

    def delete(self, request, pk: int):
        exhibition = self.get_exhibition(pk=pk)
        if exhibition is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        exhibition.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class ExhibitionFloorAPIView(APIView):
    def get(self, request):
        user_id = request.auth.payload['user_id']
        exhibitions = Exhibition.objects.filter(user_id=user_id)
        if exhibitions.count() == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        floors = []
        for exhibition in exhibitions:
            floors.append(exhibition.floor_ko)
        floors = list(set(floors))
        return Response({
            'result': floors
        }, status=status.HTTP_200_OK)


class ExhibitionListAPIView(ListAPIView):
    pagination_class = ExhibitionSetPagination
    serializer_class = ExhibitionSerializer

    def get_queryset(self):
        user_pk = self.kwargs['user_pk']
        queryset = Exhibition.objects.filter(user_id=user_pk)
        queryset = self.filter_queryset(queryset)
        return queryset

    def filter_queryset(self, queryset):
        return queryset


class InnerExhibitionAPIView(APIView):
    @staticmethod
    def get_exhibition(pk: int):
        try:
            return Exhibition.objects.get(id=pk)
        except Exhibition.DoesNotExist:
            return None

    def get(self, request, exhibition_pk):
        exhibition = self.get_exhibition(pk=exhibition_pk)
        if exhibition is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        inner_exhibition = exhibition.inner_exhibition.all()
        serializer_cls = InnerExhibitionSerializer(inner_exhibition, many=True)
        return Response(
            serializer_cls.data,
            status=status.HTTP_200_OK
        )

    def post(self, request, exhibition_pk):
        exhibition = self.get_exhibition(pk=exhibition_pk)
        if exhibition is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        serializer_cls = InnerExhibitionSerializer(data=request.data)

        if serializer_cls.is_valid():
            serializer_cls.save(exhibition=exhibition)
            return Response(
                serializer_cls.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer_cls.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class InnerExhibitionDetailAPIView(APIView):
    @staticmethod
    def get_inner_exhibition(pk: int):
        try:
            return InnerExhibition.objects.get(pk=pk)
        except InnerExhibition.DoesNotExist:
            return None

    def get(self, request, pk):
        inner_exhibition = self.get_inner_exhibition(pk=pk)
        if inner_exhibition is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        serializer_cls = InnerExhibitionSerializer(inner_exhibition)
        return Response(
            serializer_cls.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):
        inner_exhibition = self.get_inner_exhibition(pk=pk)
        if inner_exhibition is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        serializer_cls = InnerExhibitionSerializer(inner_exhibition, data=request.data)
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
        inner_exhibition = self.get_inner_exhibition(pk=pk)
        if inner_exhibition is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        inner_exhibition.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class InnerExhibitionListAPIView(ListAPIView):
    pagination_class = InnerExhibitionSetPagination
    serializer_class = InnerExhibitionSerializer

    def get_queryset(self):
        user_pk = self.kwargs['user_pk']
        queryset = InnerExhibition.objects.filter(exhibition__user_id=user_pk)
        queryset = self.filter_queryset(queryset)
        return queryset

    def filter_queryset(self, queryset):
        floor = self.request.GET.get('floor')
        if floor:
            query_object = Q()
            query_object.add(Q(exhibition__floor_en=floor), Q.OR)
            queryset = queryset.filter(query_object)
            return queryset
        return queryset

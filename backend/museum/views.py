# -*- coding:utf-8 -*-
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *


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


class InnerExhibitionByUser(APIView):
    def get(self, request, user_pk):
        inner_exhibition = InnerExhibition.objects.filter(exhibition__user_id=user_pk)
        if inner_exhibition is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        serializer_cls = InnerExhibitionSerializer(inner_exhibition, many=True)

        return Response(
            serializer_cls.data,
            status=status.HTTP_200_OK
        )
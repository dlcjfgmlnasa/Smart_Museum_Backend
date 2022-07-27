# -*- coding:utf-8 -*-
from museum.models import InnerExhibition
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import BeaconSerializer


class BeaconAPIView(APIView):
    def get(self, request):
        return Response(
            status=status.HTTP_200_OK
        )

    def put(self, request):
        return Response(
            status=status.HTTP_200_OK
        )

    def delete(self, request):
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class BeaconAPIView2(APIView):
    def post(self, request, inner_exhibition_pk):
        try:
            inner_exhibition = InnerExhibition.objects.get(pk=inner_exhibition_pk)
        except InnerExhibition.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        serializer_cls = BeaconSerializer(data=request.data)
        if serializer_cls.is_valid():
            serializer_cls.save(
                inner_exhibition=inner_exhibition
            )
            return Response(
                serializer_cls.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer_cls.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

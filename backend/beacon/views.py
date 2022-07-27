# -*- coding:utf-8 -*-
from beacon.models import Beacon
from museum.models import InnerExhibition
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import BeaconSerializer, LogSerializer
from django.utils import timezone


class BeaconAPIView(APIView):
    @staticmethod
    def get_beacon(uuid):
        try:
            beacon = Beacon.objects.get(uuid=uuid)
            return beacon
        except Beacon.DoesNotExist:
            return None

    def get(self, request):
        uuid = request.GET['uuid']
        beacon = self.get_beacon(uuid=uuid)

        if beacon is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        serializer_cls = BeaconSerializer(beacon)
        return Response(
            serializer_cls.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request):
        uuid = request.GET['uuid']
        beacon = self.get_beacon(uuid=uuid)

        if beacon is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        beacon.delete()
        beacon.save()
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


class LogAPIView(APIView):
    def post(self, request):
        uuid = request.GET['uuid']
        try:
            beacon = Beacon.objects.get(uuid=uuid)
        except Beacon.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        serializer_cls = LogSerializer(data=request.data)
        if serializer_cls.is_valid():
            serializer_cls.save(beacon=beacon)
            beacon.recent_reception = timezone.now()
            beacon.save()

            return Response(
                serializer_cls.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer_cls.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
# -*- coding:utf-8 -*-
from django.db import utils
from history.models import Log
from beacon.models import Beacon
from museum.models import InnerExhibition, Exhibition
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from beacon.serializer import BeaconSerializer
from museum.serializer import InnerExhibitionSimpleSerializer, SimpleExhibitionSerializer
from rest_framework.permissions import AllowAny
from history.serializer import LogSerializer
from django.utils import timezone


class LogAPIView(APIView):
    permission_classes = [AllowAny]

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


class BeaconAPIView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get_beacon(uuid):
        try:
            beacon = Beacon.objects.get(uuid=uuid)
            return beacon
        except Beacon.DoesNotExist:
            return None

    @staticmethod
    def random_get_beacon():
        import random
        beacons = Beacon.objects.all()
        size = len(beacons)
        i = random.choice(list(range(size)))
        beacon = beacons[i]
        return beacon

    def get(self, request):
        uuid = request.GET['uuid']
        beacon = self.get_beacon(uuid=uuid)
        # beacon = self.random_get_beacon()   # TODO: !!!반드시 바꿔야된다.

        if beacon is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        serializer_cls = BeaconSerializer(beacon)
        data = serializer_cls.data
        inner_exhibition = InnerExhibition.objects.get(pk=data['inner_exhibition'])
        exhibition = Exhibition.objects.get(pk=inner_exhibition.exhibition.id)
        inner_exhibition_info = InnerExhibitionSimpleSerializer(inner_exhibition).data
        exhibition_info = SimpleExhibitionSerializer(exhibition).data

        data['inner_exhibition'] = inner_exhibition_info
        data['inner_exhibition']['exhibition'] = exhibition_info
        return Response(
            data,
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
    permission_classes = [AllowAny]

    def post(self, request, inner_exhibition_pk):
        try:
            inner_exhibition = InnerExhibition.objects.get(pk=inner_exhibition_pk)
        except InnerExhibition.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        beacon_list = []
        uuid_list = request.data['uuid'].split(',')

        for uuid in uuid_list:
            try:
                beacon = Beacon.objects.create(
                    uuid=uuid,
                    inner_exhibition=inner_exhibition
                )
                beacon_list.append(beacon.id)
            except utils.IntegrityError:
                result = {
                    'error': '존재하는 uuid 입니다.'
                }
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

        beacons = Beacon.objects.filter(pk__in=beacon_list)
        serializer_cls = BeaconSerializer(beacons, many=True)
        return Response(
            serializer_cls.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, inner_exhibition_pk):
        try:
            inner_exhibition = InnerExhibition.objects.get(pk=inner_exhibition_pk)
        except InnerExhibition.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        beacons = inner_exhibition.beacon.all()
        beacons.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class BeaconFootPrint(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        mac_address = request.GET['mac_address']

        logs = Log.objects.filter(mac_address=mac_address)
        serializer_cls = LogSerializer(logs, many=True)
        total = []
        for data in serializer_cls.data:
            inner_exhibition_pk = data['beacon']['inner_exhibition']
            total.append(inner_exhibition_pk)
        total = list(set(total))
        result = {'result': total}

        return Response(
            result,
            status=status.HTTP_200_OK
        )
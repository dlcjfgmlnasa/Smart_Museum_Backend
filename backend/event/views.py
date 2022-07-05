# -*- coding:utf-8 -*-
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Event
from museum.models import InnerExhibition, Exhibition
from event.serializer import EventNormalSerializer, EventSimpleSerializer, EventMissionSerializer
from django.contrib.auth import get_user_model


class EventAPIView(APIView):
    def get(self, request):
        user = get_user_model().objects.get(
            id=request.auth.payload['user_id']
        )
        event = user.event.all()
        serializer_cls = EventSimpleSerializer(event, many=True)
        return Response(
            serializer_cls.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):
        user = get_user_model().objects.get(
            id=request.auth.payload['user_id']
        )
        serializer_cls = EventNormalSerializer(data=request.data)
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


class EventDetailAPIView(APIView):
    @staticmethod
    def get_event(pk):
        try:
            model = Event.objects.get(pk=pk)
            return model
        except Event.DoesNotExist:
            return None

    def get(self, request, pk):
        event = self.get_event(pk=pk)
        if event is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        serializer_cls = EventSimpleSerializer(event)
        return Response(
            serializer_cls.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):
        event = self.get_event(pk=pk)
        if event is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        serializer_cls = EventSimpleSerializer(event, data=request.data)
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
        event = self.get_event(pk=pk)
        if event is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        event.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class EventMissionAPIView(APIView):
    @staticmethod
    def get_inner_exhibition(pk):
        try:
            model = InnerExhibition.objects.get(pk=pk)
            return model
        except InnerExhibition.DoesNotExist:
            return None

    def get(self, request, inner_exhibition_pk):
        inner_exhibition = self.get_inner_exhibition(pk=inner_exhibition_pk)
        if inner_exhibition is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        events = inner_exhibition.event.all()
        serializer_cls = EventSimpleSerializer(events, many=True)
        return Response(
            serializer_cls.data,
            status=status.HTTP_200_OK
        )

    def post(self, request, inner_exhibition_pk):
        inner_exhibition = self.get_inner_exhibition(pk=inner_exhibition_pk)
        if inner_exhibition is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        serializer_cls = EventMissionSerializer(data=request.data)
        if serializer_cls.is_valid():
            serializer_cls.save(type='Mission')
            event = Event.objects.get(pk=int(serializer_cls.data['pk']))
            inner_exhibition.event.add(event)
            inner_exhibition.save()

            return Response(
                serializer_cls.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer_cls.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

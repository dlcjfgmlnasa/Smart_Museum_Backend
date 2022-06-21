# -*- coding:utf-8 -*-
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Event
from museum.models import InnerExhibition
from event.serializer import EventSerializer, EventSimpleSerializer


class EventAPIView(APIView):
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

        serializer_cls = EventSerializer(data=request.data)
        if serializer_cls.is_valid():
            serializer_cls.save(inner_exhibition=inner_exhibition)

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

        serializer_cls = EventSerializer(event)
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

        serializer_cls = EventSerializer(event, data=request.data)
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


# -*- coding:utf-8 -*-
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import Event
from museum.models import InnerExhibition, Exhibition
from rest_framework.pagination import PageNumberPagination
from event.serializer import EventNormalSerializer, EventSimpleSerializer, EventMissionSerializer
from django.contrib.auth import get_user_model
from django.db.models import Q


class EventSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 1000


class EventAPIView(APIView):
    def get(self, request):
        user = get_user_model().objects.get(
            id=request.auth.payload['user_id']
        )
        event = user.event.all().order_by('-type')
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


class EventListAPIView(ListAPIView):
    pagination_class = EventSetPagination
    serializer_class = EventSimpleSerializer

    def get_queryset(self):
        event_type = self.request.GET.get('event_type')
        events = Event.objects.filter(user_id=self.request.auth.payload['user_id'])
        if event_type:
            events = events.filter(type=event_type)
        return events


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


class EventDetailAllAPIView(APIView):
    def delete(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        event.inner_exhibition.clear()
        event.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

    def put(self, request, inner_exhibition_pk):
        user = get_user_model().objects.get(
            id=self.request.auth.payload['user_id']
        )

        inner_exhibition = self.get_inner_exhibition(pk=inner_exhibition_pk)
        if inner_exhibition is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        serializer_cls = EventMissionSerializer(inner_exhibition, data=request.data)
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

    def post(self, request, inner_exhibition_pk):
        user = get_user_model().objects.get(
            id=self.request.auth.payload['user_id']
        )
        inner_exhibition = self.get_inner_exhibition(pk=inner_exhibition_pk)
        if inner_exhibition is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        serializer_cls = EventMissionSerializer(data=request.data)
        if serializer_cls.is_valid():
            serializer_cls.save(type='Mission')
            serializer_cls.save(user=user)
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


class EventMissionListView(APIView):
    @staticmethod
    def get_inner_exhibition(pk):
        try:
            model = InnerExhibition.objects.get(pk=pk)
            return model
        except InnerExhibition.DoesNotExist:
            return None

    def post(self, request):
        user = get_user_model().objects.get(
            id=self.request.auth.payload['user_id']
        )
        inner_exhibition_pk_list = request.GET.getlist('inner_exhibition', None)

        inner_exhibitions = []
        for inner_exhibition_pk in inner_exhibition_pk_list:
            inner_exhibition = self.get_inner_exhibition(pk=inner_exhibition_pk)
            if inner_exhibition is None:
                return Response(
                    status=status.HTTP_404_NOT_FOUND
                )
            inner_exhibitions.append(inner_exhibition)

        serializer_cls = EventMissionSerializer(data=request.data)
        if serializer_cls.is_valid():
            serializer_cls.save(type='Mission')
            serializer_cls.save(user=user)
            event = Event.objects.get(pk=int(serializer_cls.data['pk']))

            for inner_exhibition in inner_exhibitions:
                inner_exhibition.event.add(event)
                inner_exhibition.save()

            event.save()
            return Response(
                serializer_cls.data,
                status=status.HTTP_200_OK
            )
        return Response(
            data=serializer_cls.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class EventMissionDetailView(APIView):
    @staticmethod
    def get_inner_exhibition(pk):
        try:
            model = InnerExhibition.objects.get(pk=pk)
            return model
        except InnerExhibition.DoesNotExist:
            return None

    def put(self, request, event_pk):
        try:
            event = Event.objects.get(pk=event_pk)
        except Event.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        serializer_cls = EventMissionSerializer(event, data=request.data)
        if serializer_cls.is_valid():
            serializer_cls.save()

        event.inner_exhibition.clear()
        event.save()

        inner_exhibition_pk_list = request.GET.getlist('inner_exhibition', None)
        for inner_exhibition_pk in inner_exhibition_pk_list:
            inner_exhibition = self.get_inner_exhibition(pk=inner_exhibition_pk)
            if inner_exhibition is None:
                return Response(
                    status=status.HTTP_404_NOT_FOUND
                )
            inner_exhibition.event.add(event)
        event.save()
        return Response(
            serializer_cls.data,
            status=status.HTTP_200_OK
        )

# -*- coding:utf-8 -*-
from .models import Event
from museum.serializer import InnerExhibitionSerializer
from rest_framework.serializers import ModelSerializer


class EventSimpleSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'pk',
            'inner_exhibition',
            'name',
            'start_dt',
            'end_dt',
            'type',
            'explanation',
            'image'
        )


class EventSerializer(ModelSerializer):
    inner_exhibition = InnerExhibitionSerializer(read_only=True)

    class Meta:
        model = Event
        fields = (
            'pk',
            'inner_exhibition',
            'name',
            'start_dt',
            'end_dt',
            'type',
            'explanation',
            'image'
        )


# -*- coding:utf-8 -*-
from .models import Event
from museum.serializer import InnerExhibitionSerializer
from account.serializer import AccountSerializer
from museum.serializer import ExhibitionSerializer
from rest_framework.serializers import ModelSerializer


class EventSimpleSerializer(ModelSerializer):
    inner_exhibition = InnerExhibitionSerializer(many=True)

    class Meta:
        model = Event
        fields = (
            'pk',
            'name',
            'start_dt',
            'end_dt',
            'type',
            'explanation',
            'image',
            'inner_exhibition'
        )


class EventNormalSerializer(ModelSerializer):
    user = AccountSerializer(read_only=True)

    class Meta:
        model = Event
        fields = (
            'pk',
            'user',
            'name',
            'start_dt',
            'end_dt',
            'type',
            'explanation',
            'image'
        )


class EventMissionSerializer(ModelSerializer):
    user = AccountSerializer(read_only=True)

    class Meta:
        model = Event
        fields = (
            'pk',
            'user',
            'name',
            'start_dt',
            'end_dt',
            'type',
            'explanation',
            'image'
        )


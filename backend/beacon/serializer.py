# -*- coding:utf-8 -*-
from museum.serializer import InnerExhibitionSimpleSerializer
from beacon.models import *
from rest_framework import serializers


class BeaconSerializer(serializers.ModelSerializer):
    inner_exhibition = InnerExhibitionSimpleSerializer(read_only=True)

    class Meta:
        model = Beacon
        fields = (
            'pk',
            'inner_exhibition',
            'recent_reception',
            'uuid'
        )


class LogSerializer(serializers.ModelSerializer):
    beacon = BeaconSerializer(read_only=True)

    class Meta:
        model = Log
        fields = (
            'pk',
            'beacon',
            'sex',
            'age_group',
        )
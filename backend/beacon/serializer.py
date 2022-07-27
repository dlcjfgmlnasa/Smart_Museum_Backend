# -*- coding:utf-8 -*-
from museum.serializer import InnerExhibitionSerializer
from beacon.models import *
from rest_framework import serializers


class BeaconSerializer(serializers.ModelSerializer):
    inner_exhibition = InnerExhibitionSerializer(read_only=True)

    class Meta:
        model = Beacon
        fields = (
            'pk',
            'inner_exhibition',
            'uuid'
        )
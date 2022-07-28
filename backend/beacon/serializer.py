# -*- coding:utf-8 -*-
from beacon.models import *
from rest_framework import serializers


class BeaconSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beacon
        fields = (
            'pk',
            'inner_exhibition',
            'recent_reception',
            'uuid'
        )

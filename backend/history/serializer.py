# -*- coding:utf-8 -*-
from history.models import Log
from beacon.serializer import BeaconSerializer
from rest_framework import serializers


class LogSerializer(serializers.ModelSerializer):
    beacon = BeaconSerializer(read_only=True)

    class Meta:
        model = Log
        fields = (
            'pk',
            'beacon',
            'sex',
            'age_group',
            'mac_address'
        )
# -*- coding:utf-8 -*-
from account.models import User
from rest_framework import serializers


class AccountCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'password',
            'username',
            'museum_name',
            'museum_location',
            'payment_state',
            'service_plan'
        )
        write_only_fields = ('password', )


class AccountSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'museum_name',
            'museum_location',
            'payment_state',
            'service_plan',
        )
        write_only_fields = ('pk', 'username')





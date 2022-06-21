# -*- coding:utf-8 -*-
from account.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model


USER_MODEL = get_user_model()


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = (
            'pk',
            'password',
            'username',
            'museum_name',
            'museum_location',
            'payment_state',
            'service_plan'
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5,
            }
        }

    def create(self, validated_data):
        password = validated_data['password']
        del validated_data['password']
        user = USER_MODEL.objects.create(**validated_data)

        user.set_password(password)
        user.save()
        return user


class AccountSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = USER_MODEL
        fields = (
            'pk',
            'username',
            'museum_name',
            'museum_location',
            'payment_state',
            'service_plan',
        )
        write_only_fields = ('pk', 'username')





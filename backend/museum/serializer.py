# -*- coding:utf-8 -*-
from museum.models import *
from beacon.models import *
from rest_framework import serializers
from account.serializer import AccountSerializer
from beacon.serializer import BeaconSerializer


class InnerExhibitionSimpleSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(read_only=True)

    class Meta:
        model = InnerExhibition
        fields = (
            'pk',
            'name',
            'vr_link',
            'order',
            'explanation',
            'image',
            'x_coordinate',
            'y_coordinate'
        )


class ExhibitionSerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only=True)
    inner_exhibition = InnerExhibitionSimpleSerializer(read_only=True, many=True)

    class Meta:
        model = Exhibition
        fields = (
            'pk',
            'user',
            'floor_ko',
            'floor_en',
            'house_ko',
            'house_en',
            'drawing_image',
            'inner_exhibition'
        )


class SimpleExhibitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exhibition
        fields = (
            'pk',
            'floor_ko',
            'floor_en',
            'house_ko',
            'house_en',
            'drawing_image'
        )


class InnerExhibitionSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(read_only=True)
    exhibition = SimpleExhibitionSerializer(read_only=True)
    beacon = BeaconSerializer(read_only=True, many=True)

    class Meta:
        model = InnerExhibition
        fields = (
            'pk',
            'exhibition',
            'name',
            'vr_link',
            'order',
            'explanation',
            'image',
            'x_coordinate',
            'y_coordinate',
            'beacon'
        )

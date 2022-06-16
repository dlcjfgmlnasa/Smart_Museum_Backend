# -*- coding:utf-8 -*-
from museum.models import *
from rest_framework import serializers
from account.serializer import AccountSerializer


class ExhibitionSerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only=True)

    class Meta:
        model = Exhibition
        fields = (
            'pk',
            'user',
            'floor_ko',
            'floor_en',
            'house_ko',
            'house_en',
            'drawing_image'
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

    class Meta:
        model = InnerExhibition
        fields = (
            'pk',
            'exhibition',
            'name',
            'vr_link',
            'order',
            'explanation',
            'image'
        )

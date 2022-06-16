# -*- coding:utf-8 -*-
from django.db import models
from backend.model import TimeStampedModel
from account.models import User


class Exhibition(TimeStampedModel):
    # 사용자
    user = models.ForeignKey(
        User, null=True,
        on_delete=models.SET_NULL,
        related_name='exhibition',
        db_column='USER_ID'
    )
    # 층수 - 한글
    floor_ko = models.CharField(
        max_length=25,
        null=False,
        db_column='FLOOR_KO'
    )
    # 층수 - 영어
    floor_en = models.CharField(
        max_length=25,
        null=False,
        db_column='FLOOR_EN'
    )
    # 구분 관 - 한글
    house_ko = models.CharField(
        max_length=25,
        null=True,
        db_column='HOUSE_KO'
    )
    # 구분 관 - 영어
    house_en = models.CharField(
        max_length=25,
        null=True,
        db_column='HOUSE_EN'
    )
    # 도면 이미지
    drawing_image = models.ImageField(
        blank=True,
        db_column='DRAWING_IMAGE'
    )

    class Meta:
        db_table = 'SM_EXHIBITION'
        ordering = ['pk']


class InnerExhibition(TimeStampedModel):
    # 전시관
    exhibition = models.ForeignKey(
        Exhibition, null=True,
        on_delete=models.SET_NULL,
        related_name='inner_exhibition',
        db_column='EXHIBITION_ID'
    )
    # 내부 전시관 이름
    name = models.CharField(
        max_length=100,
        null=False, blank=False,
        db_column='NAME'
    )
    # VR 링크 URL
    vr_link = models.URLField(
        null=True,
        db_column='VR_LINK'
    )
    # 번호 순서
    order = models.IntegerField(
        primary_key=True,
        db_column='ORDER'
    )
    # 전시관 설명
    explanation = models.TextField(
        null=True, blank=True,
        db_column='EXPLANATION'
    )
    # 내부 이미지
    image = models.ImageField(
        null=True,
        db_column='IMAGE'
    )

    class Meta:
        db_table = 'SM_INNER_EXHIBITION'
        ordering = ['pk', 'order']


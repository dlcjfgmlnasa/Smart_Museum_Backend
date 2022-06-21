# -*- coding:utf-8 -*-
from django.db import models
from backend.model import TimeStampedModel
from museum.models import InnerExhibition


class Event(TimeStampedModel):
    EVENT_CHOICE = (
        (1, 'Normal'),
        (2, 'Mission')
    )
    # 내부 전시관 아이디
    inner_exhibition = models.ForeignKey(
        InnerExhibition, null=True,
        on_delete=models.SET_NULL,
        related_name='event',
        db_column='INNER_EXHIBITION_ID'
    )
    # 이벤트 이름
    name = models.CharField(
        max_length=100,
        blank=False, null=False,
        db_column='EVENT_NAME'
    )
    # 이벤트 시작 날짜 및 시간
    start_dt = models.DateTimeField(
        blank=False, null=False,
        db_column='START_DATETIME'
    )
    # 이벤트 끝 날짜 및 시간
    end_dt = models.DateTimeField(
        blank=False, null=False,
        db_column='END_DATETIME'
    )
    # 이벤트 타입
    type = models.CharField(
        default='Normal',
        null=False, blank=False,
        max_length=25,
        choices=EVENT_CHOICE,
        db_column='TYPE'
    )
    # 전시관 설명
    explanation = models.TextField(
        null=True, blank=True,
        db_column='EXPLANATION'
    )
    # 이미지
    image = models.ImageField(
        null=True,
        db_column='IMAGE'
    )

    class Meta:
        db_table = 'SM_EVENT'
        ordering = ['pk']

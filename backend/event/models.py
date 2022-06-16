# -*- coding:utf-8 -*-
from django.db import models
from backend.model import TimeStampedModel


class Event(TimeStampedModel):
    EVENT_CHOICE = (
        (1, 'Normal'),
        (2, 'Mission')
    )
    # 이벤트 시작 날짜 및 시간
    start_dt = models.DateTimeField(
        blank=True, null=True,
        db_column='START_DATETIME'
    )
    # 이벤트 끝 날짜 및 시간
    end_dt = models.DateTimeField(
        blank=True, null=True,
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

# -*- coding:utf-8 -*-
from django.db import models
from backend.model import TimeStampedModel
from django.contrib.auth.models import AbstractUser


class User(AbstractUser, TimeStampedModel):
    PAYMENT_STATE_CHOICE = (
        (1, 'None'),
        (2, 'Progressing'),
        (3, 'Complete')
    )
    SERVICE_PLAN_CHOICE = (
        (1, '1M'),
        (2, '1Y'),
        (3, '3Y')
    )
    # 박물관 이름
    museum_name = models.CharField(
        max_length=100,
        null=False, blank=False,
        db_column='MUSEUM_NAME'
    )
    # 박물관 지역
    museum_location = models.CharField(
        max_length=25,
        null=False, blank=False,
        db_column='MUSEUM_LOCATION'
    )
    # 결재 상태
    payment_state = models.CharField(
        max_length=10,
        default='None',
        choices=PAYMENT_STATE_CHOICE,   # [미사용, 결제 승인 진행 중, 결제 완료]
        db_column='SERVICE_STATE'
    )
    # 서비스 플랜
    service_plan = models.CharField(
        max_length=5,
        null=True, blank=True,
        choices=SERVICE_PLAN_CHOICE,    # [1M, 1Y, 3M]
        db_column='SERVICE_PLAN'
    )

    class Meta:
        db_table = 'SM_USER'
        ordering = ['pk']

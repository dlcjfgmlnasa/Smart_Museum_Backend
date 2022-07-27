# -*- coding:utf-8 -*-
from django.db import models
from backend.model import TimeStampedModel
from museum.models import InnerExhibition


class Beacon(TimeStampedModel):
    inner_exhibition = models.ForeignKey(
        InnerExhibition, null=True,
        on_delete=models.SET_NULL,
        db_column='INNER_EXHIBITION_ID'
    )
    uuid = models.CharField(
        max_length=100, unique=True,
        null=False, blank=False,
        db_column='UUID'
    )
    recent_reception = models.DateTimeField(
        null=True, blank=False,
        db_column='RECENT_RECEPTION'
    )

    class Meta:
        db_table = 'SM_BEACON'
        ordering = ['id']
        unique_together = ['id', 'uuid']


class Log(TimeStampedModel):
    SEX_CHOICE = (
        (1, 'MALE'),
        (2, 'FEMALE')
    )
    AGE_GROUP_CHOICE = (
        (1, '10'),
        (2, '20'),
        (3, '30'),
        (4, '40'),
        (5, '50'),
    )
    beacon = models.ForeignKey(
        Beacon, null=True,
        on_delete=models.SET_NULL,
        db_column='BEACON_ID'
    )
    sex = models.CharField(
        null=False, blank=False,
        max_length=25,
        choices=SEX_CHOICE,
        db_column='SEX'
    )
    age_group = models.CharField(
        null=False, blank=False,
        max_length=25,
        choices=AGE_GROUP_CHOICE,
        db_column='AGE_GROUP'
    )

    class Meta:
        db_table = 'SM_LOG'
        ordering = ['pk']

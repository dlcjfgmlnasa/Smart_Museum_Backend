# -*- coding:utf-8 -*-
from django.db import models
from beacon.models import Beacon
from backend.model import TimeStampedModel
from museum.models import InnerExhibition, Exhibition


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
        (6, '50 >= '),
    )
    beacon = models.ForeignKey(
        Beacon, null=True,
        on_delete=models.SET_NULL,
        related_name='log',
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
    mac_address = models.CharField(
        null=False, blank=False,
        max_length=100,
        db_column='MAC_ADDRESS'
    )

    class Meta:
        db_table = 'SM_LOG'
        ordering = ['pk']


class DayLog(TimeStampedModel):
    inner_exhibition = models.ForeignKey(
        InnerExhibition, null=True,
        on_delete=models.SET_NULL,
        related_name='day_log',
        db_column='INNER_EXHIBITION_ID'
    )
    date = models.DateField(
        null=False, blank=False,
        db_column='DATE'
    )
    count = models.IntegerField(
        null=False, blank=False,
        db_column='COUNT'
    )
    sex_count = models.JSONField(
        null=False, blank=False,
        db_column='SEX_COUNT'
    )
    age_group_count = models.JSONField(
        null=False, blank=False,
        db_column='AGE_GROUP_COUNT'
    )
    time_count = models.JSONField(
        null=False, blank=False,
        db_column='TIME_COUNT'
    )

    class Meta:
        db_table = 'SM_DAY_LOG'
        ordering = ['pk']
        unique_together = ['date', 'inner_exhibition']


class FootPrintLog(TimeStampedModel):
    exhibition = models.ForeignKey(
        Exhibition, null=True,
        on_delete=models.SET_NULL,
        related_name='foot_print',
        db_column='EXHIBITION_ID'
    )
    date = models.DateField(
        null=False, blank=False,
        db_column='DATE'
    )
    foot_printing_count = models.JSONField(
        null=False, blank=False,
        db_column='FOOT_PRINT_COUNT'
    )

    class Meta:
        db_table = 'SM_FOOT_PRINT_LOG'
        ordering = ['pk']
        unique_together = ['date', 'exhibition']


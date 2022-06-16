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
    beacon_id = models.BigIntegerField(
        db_column='BEACON_ID'
    )
    recent_reception = models.DateTimeField(
        null=True, blank=False,
        db_column='REACT_RECEPTION'
    )

    class Meta:
        db_table = 'SM_BEACON'
        ordering = ['pk']

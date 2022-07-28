# -*- coding:utf-8 -*-
from django.db import models
from backend.model import TimeStampedModel
from museum.models import InnerExhibition


class Beacon(TimeStampedModel):
    inner_exhibition = models.ForeignKey(
        InnerExhibition, null=True,
        on_delete=models.SET_NULL,
        related_name='beacon',
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



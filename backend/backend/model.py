# -*- coding:utf-8 -*-
from django.db import models


class TimeStampedModel(models.Model):
    int_dt = models.DateTimeField(auto_now_add=True, db_column='INS_DT')
    upt_dt = models.DateTimeField(auto_now=True, db_column='UPD_DT')

    class Meta:
        abstract = True

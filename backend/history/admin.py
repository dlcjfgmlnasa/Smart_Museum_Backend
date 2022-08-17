# -*- coding:utf-8 -*-
from django.contrib import admin
from .models import Log, FootPrintLog, DayLog


admin.site.register(Log)
admin.site.register(FootPrintLog)
admin.site.register(DayLog)


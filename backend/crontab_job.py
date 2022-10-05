# -*- coding:utf-8 -*-
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

import django
import operator
django.setup()


from museum.models import InnerExhibition, Exhibition
from history.models import Log, DayLog, FootPrintLog
from django.utils import timezone
from datetime import timedelta


def crontab_footprint_job():
    exhibitions = Exhibition.objects.filter(user__is_superuser=False)
    date = timezone.now() - timedelta(days=1)
    date = date.strftime('%Y-%m-%d')

    foot_print_list = []
    for exhibition in exhibitions:
        total_footprint = {idx: {inner_exhibition.id: 0 for inner_exhibition in exhibition.inner_exhibition.all()}
                           for idx in range(200)}
        logs = Log.objects.filter(beacon__inner_exhibition__exhibition=exhibition)

        mac_address_list = list(set([log.mac_address for log in logs]))
        footprint__temp = {mad_address: [] for mad_address in mac_address_list}

        for mad_address in mac_address_list:
            mac_address_log = logs.filter(mac_address=mad_address).order_by('int_dt')
            footprint__temp[mad_address] = [query.beacon.inner_exhibition.id for query in mac_address_log]

        for key, values in footprint__temp.items():
            sample = [values[0]]
            count = 0
            for i, value in enumerate(values[1:]):
                if sample[count] != value:
                    sample.append(value)
                    count += 1
            for n, inner_exhibition_idx in enumerate(sample):
                total_footprint[n][inner_exhibition_idx] += 1

        result = {}
        for key, stats in total_footprint.items():
            value = max(stats.items(), key=operator.itemgetter(1))
            if value[1] == 0:
                result[key] = None
            else:
                result[key] = value[0]
        result = [v for v in result.values() if v is not None]
        foot_print_list.append(
            FootPrintLog(
                exhibition=exhibition,
                date=date,
                foot_printing_count=result
            )
        )
    FootPrintLog.objects.bulk_create(foot_print_list)


def crontab_log_day_count_job():
    inner_exhibitions = InnerExhibition.objects.all()

    day_logs = []
    for inner_exhibition in inner_exhibitions:
        total_sex = {sex_index[0]: 0 for sex_index in Log.SEX_CHOICE}
        total_age = {age_index[0]: 0 for age_index in Log.AGE_GROUP_CHOICE}

        logs = Log.objects.filter(beacon__inner_exhibition=inner_exhibition)
        mac_address_list = list(set([log.mac_address for log in logs]))
        for mad_address in mac_address_list:
            query = logs.filter(mac_address=mad_address).first()
            total_sex[int(query.sex)] = total_sex[int(query.sex)] + 1
            total_age[int(query.age_group)] = total_age[int(query.age_group)] + 1

        total_sex = {dict(Log.SEX_CHOICE)[k]: v for k, v in total_sex.items()}
        total_age = {dict(Log.AGE_GROUP_CHOICE)[k]: v for k, v in total_age.items()}
        total_time = {hour: logs.filter(int_dt__hour=hour).count() for hour in range(24)}

        date = timezone.now() - timedelta(days=1)
        date = date.strftime('%Y-%m-%d')

        day_logs.append(
            DayLog(
                inner_exhibition=inner_exhibition,
                date=date,
                count=logs.count(),
                sex_count=total_sex,
                age_group_count=total_age,
                time_count=total_time,
            )
        )
    DayLog.objects.bulk_create(day_logs)


def delete_log():
    logs = Log.objects.all()
    logs.delete()


def main_crontab():
    crontab_footprint_job()         # Job - 1 : 사용자 발자국 추적 저장
    crontab_log_day_count_job()     # Job - 2 : 사용자 정보 저장
    delete_log()                    # Job - 3 : 로그 삭제


if __name__ == '__main__':
    main_crontab()

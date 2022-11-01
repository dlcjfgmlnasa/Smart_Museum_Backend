# -*- coding:utf-8 -*-
import os
import numpy as np
import pandas as pd
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

import django
import operator
from datetime import datetime
django.setup()


from museum.models import InnerExhibition, Exhibition
from history.models import Log, DayLog, FootPrintLog
from django.utils import timezone
from datetime import timedelta


def crontab_footprint_job():
    def total_seconds(timedelta_):
        try:
            seconds = timedelta_.total_seconds()
        except AttributeError:  # no method total_seconds
            one_second = np.timedelta64(1000000000, 'ns')
            # use nanoseconds to get highest possible precision in output
            seconds = timedelta_ / one_second
        return seconds

    exhibitions = Exhibition.objects.filter(user__is_superuser=False)
    date = timezone.now() - timedelta(days=1)
    date = date.strftime('%Y-%m-%d')

    foot_print_list = []
    for exhibition in exhibitions:
        logs = Log.objects.filter(beacon__inner_exhibition__exhibition=exhibition)

        mac_address_list = list(set([log.mac_address for log in logs]))
        footprint__temp = {mad_address: [] for mad_address in mac_address_list}

        for mad_address in mac_address_list:
            mac_address_log = logs.filter(mac_address=mad_address).order_by('int_dt')
            df = pd.DataFrame(mac_address_log.values())

            times = pd.to_datetime(df['int_dt'].values[1:]) - pd.to_datetime(df['int_dt'].values[:-1])
            times = np.array([total_seconds(time) for time in times])
            times = list(times > 30)    # 30초 이상 머물렀을때
            times.append(True)

            temp = []
            for query, time in zip(mac_address_log, times):
                if time:
                    temp.append(query.beacon.inner_exhibition.id)
            footprint__temp[mad_address] = temp

        try:
            total_footprint = {
                idx: {inner_exhibition.id: 0 for inner_exhibition in exhibition.inner_exhibition.all()}
                for idx in range(max([len(v) for v in footprint__temp.values()]))}
        except ValueError:
            total_footprint = {
                idx: {inner_exhibition.id: 0 for inner_exhibition in exhibition.inner_exhibition.all()}
                for idx in range(200)
            }

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
            try:
                value = max(stats.items(), key=operator.itemgetter(1))
            except ValueError:
                continue
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


def save_csv():
    def total_seconds(_timedelta):
        try:
            seconds = _timedelta.total_seconds()
        except AttributeError:  # no method total_seconds
            one_second = np.timedelta64(1000000000, 'ns')
            # use nanoseconds to get highest possible precision in output
            seconds = _timedelta / one_second
        return seconds

    now = timezone.now() - timedelta(days=1)
    now = now.strftime('%Y-%m-%d')

    exhibitions = Exhibition.objects.filter(user__is_superuser=False)
    log_df = {'unique_id': [], 'date': [], 'start_time': [], 'end_time': [], 'path': []}
    for exhibition in exhibitions:
        logs = Log.objects.filter(beacon__inner_exhibition__exhibition=exhibition)

        mac_address_list = list(set([log.mac_address for log in logs]))

        for mac_address in mac_address_list:
            mac_address_log = logs.filter(mac_address=mac_address).order_by('int_dt')
            start_dt, end_dt = mac_address_log.first().int_dt, mac_address_log.last().int_dt
            df = pd.DataFrame(mac_address_log.values())

            times = pd.to_datetime(df['int_dt'].values[1:]) - pd.to_datetime(df['int_dt'].values[:-1])
            times = np.array([total_seconds(time) for time in times])
            times = list(times > 30)  # 30초 이상 머물렀을때
            times.append(True)

            temp = []
            for query, time in zip(mac_address_log, times):
                if time:
                    temp.append(str(query.beacon.inner_exhibition.id))

            temp2 = []
            for i, pk in enumerate(temp):
                if i == 0:
                    temp2.append(str(pk))
                else:
                    if temp2[len(temp2) - 1] != pk:
                        temp2.append(str(pk))
            path = '-'.join(temp2)
            date = start_dt.strftime('%Y-%m-%d')
            start_time, end_time = start_dt.strftime('%H:%M:%S'), end_dt.strftime('%H:%M:%S')

            log_df['unique_id'].append(mac_address)
            log_df['date'].append(date)
            log_df['start_time'].append(start_time)
            log_df['end_time'].append(end_time)
            log_df['path'].append(path)

    foot_print_df = pd.DataFrame(log_df)
    foot_print_df.to_csv(
        os.path.join('.', 'log_files', 'foot_print', '{}_Foot_Print_Log.csv'.format(now)),
        index=False
    )

    total_df = {'int_dt': [], 'upt_dt': [], 'beacon_id': [], 'sex': [], 'age_group': [], 'mac_address': []}
    exhibitions = Exhibition.objects.filter(user__is_superuser=False)
    for exhibition in exhibitions:
        logs = Log.objects.filter(beacon__inner_exhibition__exhibition=exhibition)
        try:
            df = pd.DataFrame(logs.values())[['int_dt', 'upt_dt', 'beacon_id', 'sex', 'age_group', 'mac_address']]
        except KeyError:
            continue

        total_df['int_dt'].extend(df['int_dt'].values)
        total_df['upt_dt'].extend(df['upt_dt'].values)
        total_df['beacon_id'].extend(df['beacon_id'].values)
        total_df['sex'].extend(df['sex'].values)
        total_df['age_group'].extend(df['age_group'].values)
        total_df['mac_address'].extend(df['mac_address'].values)

    total_df = pd.DataFrame(total_df)
    total_df.to_csv(
        os.path.join('.', 'log_files', 'log', '{}_Raw.csv'.format(now)),
        index=False
    )


def delete_log():
    logs = Log.objects.all()
    logs.delete()


def main_crontab():
    crontab_footprint_job()         # Job - 1 : 사용자 발자국 추적 저장
    crontab_log_day_count_job()     # Job - 2 : 사용자 정보 저장
    save_csv()                      # Job - 3 : 로그 저장
    delete_log()                    # Job - 4 : 로그 삭제


if __name__ == '__main__':
    main_crontab()

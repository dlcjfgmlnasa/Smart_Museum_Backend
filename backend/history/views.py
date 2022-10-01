# -*- coding:utf-8 -*-
from datetime import datetime
from museum.serializer import InnerExhibitionSimpleSerializer
from museum.models import Exhibition, InnerExhibition
from history.models import Log, DayLog, FootPrintLog
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import operator


class ExhibitionDayAPIView(APIView):
    def get(self, request, exhibition_pk):
        try:
            exhibition = Exhibition.objects.get(pk=exhibition_pk)
        except Exhibition.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            date = request.GET['date']
            year, month, day = date.split('-')
            month = '{0:02d}'.format(int(month))
            day = '{0:02d}'.format(int(day))
            date = year + '-' + month + '-' + day
            date = datetime.fromisoformat(date)
        except KeyError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )

        now = datetime.now()
        if now.year == date.year and now.month == date.month and now.day == date.day:
            inner_exhibitions = exhibition.inner_exhibition.all()
            queryset = Log.objects.filter(
                beacon__inner_exhibition__in=inner_exhibitions,
                int_dt__year=date.year, int_dt__month=date.month, int_dt__day=date.day
            )
            queryset = queryset.filter()
            total_sex = {sex_index[0]: 0 for sex_index in Log.SEX_CHOICE}
            total_age = {age_index[0]: 0 for age_index in Log.AGE_GROUP_CHOICE}

            for query in queryset:
                total_sex[int(query.sex)] = total_sex[int(query.sex)] + 1
                total_age[int(query.sex)] = total_age[int(query.sex)] + 1

            total_sex = {dict(Log.SEX_CHOICE)[k]: v for k, v in total_sex.items()}
            total_age = {dict(Log.AGE_GROUP_CHOICE)[k]: v for k, v in total_age.items()}

            result = {
                'audience': queryset.count(),
                'sex': total_sex,
                'age': total_age
            }
            return Response(result, status=status.HTTP_200_OK)
        else:
            inner_exhibitions = exhibition.inner_exhibition.all()
            total_sex = {sex_index[1]: 0 for sex_index in Log.SEX_CHOICE}
            total_age = {age_index[1]: 0 for age_index in Log.AGE_GROUP_CHOICE}

            try:
                for inner_exhibition in inner_exhibitions:
                    log = DayLog.objects.get(
                        inner_exhibition_id=inner_exhibition.id,
                        date__year=date.year, date__month=date.month, date__day=date.day
                    )
                    for k, v in log.sex_count.items():
                        total_sex[k] += v

                    for k, v in log.age_group_count.items():
                        total_age[k] += v

                audience = sum(total_age.values())
                result = {
                    'audience': audience,
                    'sex': total_sex,
                    'age': total_age
                }
                return Response(result, status=status.HTTP_200_OK)
            except DayLog.DoesNotExist:
                result = {
                    'audience': 0,
                    'sex': total_sex,
                    'age': total_age
                }
                return Response(result, status=status.HTTP_200_OK)


class ExhibitionPopularityAPIView(APIView):
    def get(self, request, exhibition_pk):
        try:
            exhibition = Exhibition.objects.get(pk=exhibition_pk)
        except Exhibition.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        total = []
        inner_exhibitions = exhibition.inner_exhibition.all()
        for inner_exhibition in inner_exhibitions:
            # 누적 박물관 관람객 정보 + 현재 박물관 관람객 정보
            day_logs = DayLog.objects.filter(inner_exhibition_id=inner_exhibition.id)
            logs = Log.objects.filter(beacon__inner_exhibition=inner_exhibition.id)
            current_age = {age_index[0]: 0 for age_index in Log.AGE_GROUP_CHOICE}
            for query in logs:
                current_age[int(query.sex)] = current_age[int(query.sex)] + 1

            current_age = {dict(Log.AGE_GROUP_CHOICE)[k]: v for k, v in current_age.items()}

            for day_log in day_logs:
                for k, value in day_log.age_group_count.items():
                    current_value = current_age[k]
                    total.append({'name': inner_exhibition.name,
                                  'age_group': k,
                                  'count': value + current_value})

        total = sorted(total, key=lambda x: x['count'], reverse=True)
        n_total = []
        for i, sample in enumerate(total):
            sample['rank'] = i + 1
            n_total.append(sample)

        return Response(
            n_total,
            status=status.HTTP_200_OK
        )


class ExhibitionTimeAPIView(APIView):
    def get(self, request, exhibition_pk):
        try:
            exhibition = Exhibition.objects.get(pk=exhibition_pk)
        except Exhibition.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            date = request.GET['date']
            year, month, day = date.split('-')
            month = '{0:02d}'.format(int(month))
            day = '{0:02d}'.format(int(day))
            date = year + '-' + month + '-' + day
            date = datetime.fromisoformat(date)
        except KeyError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        now = datetime.now()
        inner_exhibitions = exhibition.inner_exhibition.all()
        times = {str(hour): [] for hour in range(24)}

        if now.year == date.year and now.month == date.month and now.day == date.day:
            for inner_exhibition in inner_exhibitions:
                logs = Log.objects.filter(beacon__inner_exhibition=inner_exhibition.id)
                current_time = {str(hour): logs.filter(int_dt__hour=hour).count() for hour in range(24)}
                for k, v in current_time.items():
                    times[k].append(v)
        else:
            for inner_exhibition in inner_exhibitions:
                day_logs = DayLog.objects.filter(
                    inner_exhibition_id=inner_exhibition.id,
                    date__year=date.year, date__month=date.month, date__day=date.day
                )
                for day_log in day_logs:
                    time_count = day_log.time_count
                    for k, v in time_count.items():
                        times[k].append(v)
        times = {k: sum(v) for k, v in times.items()}
        return Response(
            times,
            status=status.HTTP_200_OK
        )


class ExhibitionFootPrintAPIView(APIView):
    def get(self, request, exhibition_pk):
        try:
            exhibition = Exhibition.objects.get(pk=exhibition_pk)
        except Exhibition.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            date = request.GET['date']
            year, month, day = date.split('-')
            month = '{0:02d}'.format(int(month))
            day = '{0:02d}'.format(int(day))
            date = year + '-' + month + '-' + day
            date = datetime.fromisoformat(date)
        except KeyError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        now = datetime.now()
        if now.year == date.year and now.month == date.month and now.day == date.day:
            total_footprint = {
                idx: {inner_exhibition.id: 0 for inner_exhibition in exhibition.inner_exhibition.all()}
                for idx in range(50)}
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
            result_pk_list = [v for v in result.values() if v is not None]
        else:
            try:
                foot_print = FootPrintLog.objects.get(
                    exhibition=exhibition,
                    date__year=date.year, date__month=date.month, date__day=date.day
                )
            except FootPrintLog.DoesNotExist:
                return Response(
                    status=status.HTTP_404_NOT_FOUND
                )
            result_pk_list = foot_print.foot_printing_count
        contents = []
        for rank, inner_exhibition_pk in enumerate(result_pk_list):
            inner_exhibition = InnerExhibition.objects.get(pk=inner_exhibition_pk)
            contents.append({
                'rank': rank+1,
                'inner_exhibitions': InnerExhibitionSimpleSerializer(inner_exhibition).data
            })
        contents = contents[:10]    # top 10
        return Response(contents, status=status.HTTP_200_OK)


class InnerExhibitionDayAPIView(APIView):
    def get(self, request, inner_exhibition_pk):
        try:
            inner_exhibition = InnerExhibition.objects.get(pk=inner_exhibition_pk)
        except InnerExhibition.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            date = request.GET['date']
            year, month, day = date.split('-')
            month = '{0:02d}'.format(int(month))
            day = '{0:02d}'.format(int(day))
            date = year + '-' + month + '-' + day
            date = datetime.fromisoformat(date)
        except KeyError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        now = datetime.now()
        if now.year == date.year and now.month == date.month and now.day == date.day:
            logs = Log.objects.filter(beacon__inner_exhibition=inner_exhibition.id)
            total_sex = {sex_index[0]: 0 for sex_index in Log.SEX_CHOICE}
            total_age = {age_index[0]: 0 for age_index in Log.AGE_GROUP_CHOICE}

            for log in logs:
                total_sex[int(log.sex)] = total_sex[int(log.sex)] + 1
                total_age[int(log.sex)] = total_age[int(log.sex)] + 1

            total_sex = {dict(Log.SEX_CHOICE)[k]: v for k, v in total_sex.items()}
            total_age = {dict(Log.AGE_GROUP_CHOICE)[k]: v for k, v in total_age.items()}

            result = {
                'audience': logs.count(),
                'sex': total_sex,
                'age': total_age
            }

            return Response(
                result,
                status=status.HTTP_200_OK
            )
        else:
            try:
                day_logs = DayLog.objects.get(
                    inner_exhibition_id=inner_exhibition.id,
                    date__year=date.year, date__month=date.month, date__day=date.day
                )
            except DayLog.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            result = {
                'audience': sum(day_logs.sex_count.values()),
                'sex': day_logs.sex_count,
                'age': day_logs.age_group_count
            }
            return Response(
                result,
                status=status.HTTP_200_OK
            )


class InnerExhibitionTimeAPIView(APIView):
    def get(self, request, inner_exhibition_pk):
        try:
            inner_exhibition = InnerExhibition.objects.get(pk=inner_exhibition_pk)
        except InnerExhibition.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            date = request.GET['date']
            year, month, day = date.split('-')
            month = '{0:02d}'.format(int(month))
            day = '{0:02d}'.format(int(day))
            date = year + '-' + month + '-' + day
            date = datetime.fromisoformat(date)
        except KeyError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        now = datetime.now()
        times = {str(hour): [] for hour in range(24)}
        if now.year == date.year and now.month == date.month and now.day == date.day:
            logs = Log.objects.filter(beacon__inner_exhibition=inner_exhibition.id)
            current_time = {str(hour): logs.filter(int_dt__hour=hour).count() for hour in range(24)}
            for k, v in current_time.items():
                times[k].append(v)
        else:
            day_logs = DayLog.objects.filter(
                inner_exhibition_id=inner_exhibition.id,
                date__year=date.year, date__month=date.month, date__day=date.day
            )
            for day_log in day_logs:
                time_count = day_log.time_count
                for k, v in time_count.items():
                    times[k].append(v)

        times = {k: sum(v) for k, v in times.items()}
        return Response(
            times,
            status=status.HTTP_200_OK
        )
import pandas as pd
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from andorcal.time_dict import create_time_dict
import itertools as its


def datetime_range(start, end, end_is_dst=False, delta=timedelta(minutes=15), include=False, as_utc=False):
    """Datetime Generator

    Creates a datetime range generator from `start` to `end`

    `as_utc`=True implicitly means that input datetimes are CET/CEST and will be converted to UTC"""
    if as_utc:
        local_tz = ZoneInfo('CET')
        utc_tz = ZoneInfo('UTC')
        local_start = start.replace(tzinfo=local_tz)
        local_end = end.replace(fold=int(not end_is_dst), tzinfo=local_tz)
        start = local_start.astimezone(utc_tz)
        end = local_end.astimezone(utc_tz)

        # dst_start_1 = dst_dates(start).utc()[0]
        # dst_start_2 = dst_dates(end).utc()[0]

        # skip1 = (dst_start_1 >= start) and (dst_start_1 <= end)
        # skip2 = (dst_start_2 >= start) and (dst_start_2 <= end)

        current = start
        if include:
            while current <= end:
                # if skip1 and current == dst_start_1:
                #     current += delta
                #     continue
                # elif skip2 and current == dst_start_2:
                #     current += delta
                #     continue

                yield current
                current += delta
        else:
            while current < end:
                # if skip1 and current == dst_start_1:
                #     continue
                # elif skip2 and current == dst_start_2:
                #     continue

                yield current
                current += delta
    else:
        current = start
        if include:
            while current <= end:
                yield current
                current += delta
        else:
            while current < end:
                yield current
                current += delta


def datetime_range_to_calendar(datetime_range, interval_in_minutes: int):
    """Converts a list of UTC datetimes to a calender. If an interval is provided
    then we also get the until-times"""
    records = list()
    for dt in datetime_range:
        records.append(create_time_dict(time=dt, interval_in_minutes=interval_in_minutes))
    df = pd.DataFrame.from_records(records)
    return df


def create_calendar(from_year,
                    from_month,
                    from_day,
                    until_year,
                    until_month,
                    until_day,
                    interval_in_minutes):
    """Creates a dataframe with al the times, timezone and other helper columns
    for a range of dates"""
    dts = [dt for dt in datetime_range(
        datetime(from_year, from_month, from_day),
        datetime(until_year, until_month, until_day),
        delta=timedelta(minutes=interval_in_minutes),
        as_utc=True)]

    df = datetime_range_to_calendar(dts, interval_in_minutes)

    # Post-process Add hour of day and ISP
    if 'ISP' in df.columns:
        hod = list()
        isp = list()

        for day, grouped in df.groupby('day_date'):
            duration = (
                grouped.from_CEST_time.iloc[grouped.shape[0]-1] -
                grouped.from_CEST_time.iloc[0]) + pd.Timedelta(minutes=interval_in_minutes)

            # seconds to hours
            duration = int(duration.total_seconds() // 3600)

            hod += [[i]*(60//interval_in_minutes) for i in range(1, duration+1)]
            isp_list = [i for i in range(1, (duration*4)+1)]
            isp += list(its.islice(isp_list, None, None, interval_in_minutes//15))

        df.hourofday = pd.Series(its.chain.from_iterable(hod))
        df.ISP = pd.Series(isp)

    return df

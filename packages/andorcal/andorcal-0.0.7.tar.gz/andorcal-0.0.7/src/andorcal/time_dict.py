from datetime import (timedelta, datetime)
from zoneinfo import ZoneInfo
from typing import Union

from andorcal.dst import dst_dates
from andorcal import const


def create_time_dict(
        time: Union[str, datetime], interval_in_minutes: int = 15):
    """From a time string or a datetime, create relevant calander
    data. The date_time_aware object is used as basis for all derivative 
    information.

    When time is ambiguous or naive, we assume a UTC timezone.

    Args:
        time (str or datetime): time string in ISO 8601.

    Returns:
        dict: all kinds of calendar data. 
    """
    # Create the basis information (date_time_aware)
    local_tz = const.tz

    if isinstance(time, str):
        time = datetime.fromisoformat(time)

    if time.tzinfo is None:
        time = time.replace(tzinfo=ZoneInfo('UTC'))

    if time.tzinfo == ZoneInfo('UTC'):
        utc_time = time
        date_time_aware = time.astimezone(local_tz)
        clocktime = date_time_aware.replace(tzinfo=None)

    elif time.tzinfo == local_tz or time.tzinfo == ZoneInfo('Europe/Amsterdam'):
        utc_time = time.astimezone(ZoneInfo('UTC'))
        date_time_aware = time
        clocktime = time.replace(tz=None)

    else:
        raise ValueError(f"Input is of unsupported TZ {time.tzinfo}")

    is_dst = date_time_aware.utcoffset() > timedelta(hours=1)

    # if utctime:
    #     basetimestamp = utctime
    #     current_tz = ZoneInfo('UTC')
    #     if utctime.tzinfo is None:
    #         utc_time = basetimestamp
    #     elif basetimestamp.tzinfo == current_tz:
    #         utc_time = utctime
    #     else:
    #         raise ValueError()
    #     date_time_aware = utc_time.astimezone(local_tz)
    #     clocktime = date_time_aware.replace(tzinfo=None)
    #     dst = dst_dates(utctime)
    #     is_dst = dst.is_dst
    # else:
    #     basetimestamp = timestamp
    #     utc_time = datetime.strptime(basetimestamp, datetime_fmt).replace(tzinfo=ZoneInfo('UTC'))
    #     date_time_aware = utc_time.astimezone(local_tz)
    #     clocktime = date_time_aware.replace(tzinfo=None)
    #     dst = dst_dates(date_time_aware)
    #     is_dst = dst.is_dst(utctime)

    #     dst_start, dst_stop = dst.cest()
    #     is_start = date_time_aware == dst_start
    #     is_end = date_time_aware == dst_stop

    cesttime = date_time_aware

    month_start = datetime.strptime(datetime.strftime(
        date_time_aware.replace(day=1),
        const.month_start_time_fmt), const.month_start_time_fmt)
    next_month = date_time_aware.replace(day=28) + timedelta(days=4)
    month_end_day = next_month - timedelta(days=next_month.day)
    month_end = datetime.strptime(datetime.strftime(
        month_end_day, const.month_end_time_fmt), const.datetime_fmt)

    year_start = datetime(date_time_aware.year, 1, 1, 0, 0, 0, 0, tzinfo=local_tz)
    td_from_yearstart = date_time_aware.timestamp() - year_start.timestamp()

    day_start = datetime.strptime(datetime.strftime(
        date_time_aware, const.daytime_fmt), const.daytime_fmt)
    td_from_daystart = date_time_aware.timestamp() - day_start.timestamp()
    # Determine day-night hours and calader stuff like holidays
    year_public_holidays = const.public_holidays[str(date_time_aware.year)]
    year_off_peak_holidays = const.off_peak_holidays[str(date_time_aware.year)]

    date = date_time_aware.date()
    is_public_holiday = (date in year_public_holidays)
    is_off_peak_holiday = (date in year_off_peak_holidays)
    is_weekend = (date_time_aware.timetuple().tm_wday) > 5

    is_low_hour_normal = (date_time_aware.hour <=
                          const.last_low_hour or date_time_aware.hour >=
                          const.first_low_hour_normal)
    is_low_hour_south = (date_time_aware.hour <=
                         const.last_low_hour or date_time_aware.hour >=
                         const.first_low_hour_south)
    is_low_tariff_normal = (
        is_weekend or is_off_peak_holiday or is_low_hour_normal)
    is_low_tariff_south = (
        is_weekend or is_off_peak_holiday or is_low_hour_south)

    until_CEST_time = (utc_time + timedelta(minutes=interval_in_minutes)).astimezone(local_tz)

    if interval_in_minutes == 15:
        time_dict = {
            'timestamp': clocktime,
            'from_CEST_time': cesttime,
            'until_CEST_time': until_CEST_time,
            'utctime': utc_time,
            'day_date': date,
            'month_start': month_start,
            'month_end': month_end,
            'year': date_time_aware.year,
            'month': date_time_aware.month,
            'monthyear': date_time_aware.strftime(const.year_month_fmt),
            'day': date_time_aware.day,
            'dayofweek': date_time_aware.timetuple().tm_wday + 1,
            'dayofyear': date_time_aware.timetuple().tm_yday,
            'hour': date_time_aware.hour,
            'hourofday': int(td_from_daystart/3600) + 1,
            'hourofyear': int(td_from_yearstart/3600) + 1,
            'ISP': int(td_from_daystart/900) + 1,
            'is_dst': 1 if is_dst else 0,
            'is_weekend': 1 if is_weekend else 0,
            'is_off_peak_holiday': 1 if is_off_peak_holiday else 0,
            'is_public_holiday': 1 if is_public_holiday else 0,
            'is_special_day': None,
            'is_school_holiday_south': None,
            'is_school_holiday_mid': None,
            'is_school_holiday_north': None,
            'is_low_hour_normal': 1 if is_low_hour_normal else 0,
            'is_low_hour_south': 1 if is_low_hour_south else 0,
            'is_low_tariff_normal': 1 if is_low_tariff_normal else 0,
            'is_low_tariff_south': 1 if is_low_tariff_south else 0}
    elif interval_in_minutes == 60:
        time_dict = {
            'timestamp': clocktime,
            'from_CEST_time': cesttime,
            'until_CEST_time': until_CEST_time,
            'utctime': utc_time,
            'day_date': date,
            'month_start': month_start,
            'month_end': month_end,
            'year': date_time_aware.year,
            'month': date_time_aware.month,
            'monthyear': date_time_aware.strftime(const.year_month_fmt),
            'day': date_time_aware.day,
            'dayofweek': date_time_aware.timetuple().tm_wday + 1,
            'dayofyear': date_time_aware.timetuple().tm_yday,
            'hour': date_time_aware.hour,
            'hourofday':  int(td_from_daystart/3600) + 1,  # on DST day 03:00 is the third hour, not the 4th
            'hourofyear': int(td_from_yearstart/3600) + 1,
            'is_dst': 1 if is_dst else 0,
            'is_weekend': 1 if is_weekend else 0,
            'is_off_peak_holiday': 1 if is_off_peak_holiday else 0,
            'is_public_holiday': 1 if is_public_holiday else 0,
            'is_special_day': None,
            'is_school_holiday_south': None,
            'is_school_holiday_mid': None,
            'is_school_holiday_north': None,
            'is_low_hour_normal': 1 if is_low_hour_normal else 0,
            'is_low_hour_south': 1 if is_low_hour_south else 0,
            'is_low_tariff_normal': 1 if is_low_tariff_normal else 0,
            'is_low_tariff_south': 1 if is_low_tariff_south else 0}
    elif interval_in_minutes == 1440:
        time_dict = {
            'timestamp': clocktime,
            'from_CEST_time': cesttime,
            'until_CEST_time': until_CEST_time,
            'utctime': utc_time,
            'day_date': date,
            'month_start': month_start,
            'month_end': month_end,
            'year': date_time_aware.year,
            'month': date_time_aware.month,
            'monthyear': date_time_aware.strftime(const.year_month_fmt),
            'day': date_time_aware.day,
            'dayofweek': date_time_aware.timetuple().tm_wday + 1,
            'dayofyear': date_time_aware.timetuple().tm_yday,
            'is_dst': 1 if is_dst else 0,
            'is_weekend': 1 if is_weekend else 0,
            'is_off_peak_holiday': 1 if is_off_peak_holiday else 0,
            'is_public_holiday': 1 if is_public_holiday else 0,
            'is_special_day': None,
            'is_school_holiday_south': None,
            'is_school_holiday_mid': None,
            'is_school_holiday_north': None,
            'is_low_hour_normal': 1 if is_low_hour_normal else 0,
            'is_low_hour_south': 1 if is_low_hour_south else 0,
            'is_low_tariff_normal': 1 if is_low_tariff_normal else 0,
            'is_low_tariff_south': 1 if is_low_tariff_south else 0}
    else:
        raise ValueError('Time interval must be one of [15, 60, 1440]')

    return time_dict

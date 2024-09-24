from andorcal.time_dict import create_time_dict
from andorcal.const import year_month_fmt
from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo

def test_timedict_utc_15():

    cest = ZoneInfo('CET')
    utc = ZoneInfo('UTC')
    input = datetime(2024, 3, 31, 1, tzinfo=utc)

    out = create_time_dict(time=input, interval_in_minutes=15)

    model = {
        'timestamp': datetime(2024, 3, 31, 3),
        'from_CEST_time': datetime(2024, 3, 31, 3, tzinfo=cest),
        'until_CEST_time': datetime(2024, 3, 31, 3, tzinfo=cest) + timedelta(seconds=900),
        'utctime': datetime(2024, 3, 31, 1, tzinfo=utc),
        'day_date': date(2024, 3, 31),
        'month_start': datetime(2024, 3, 1),
        'month_end': datetime(2024, 3, 31, 23, 59, 59),
        'year': 2024,
        'month': 3,
        'monthyear': "March 24",
        'day': 31,
        'dayofweek': 7,
        'dayofyear': 91,
        'hour': 3,
        'hourofday': 3,
        'hourofyear': 2163,
        'ISP': 9,
        'is_dst': 1,
        'is_weekend': 1,
        'is_off_peak_holiday': 0,
        'is_public_holiday': 0,
        'is_special_day': None,
        'is_school_holiday_south': None,
        'is_school_holiday_mid': None,
        'is_school_holiday_north': None,
        'is_low_hour_normal': 1,
        'is_low_hour_south': 1,
        'is_low_tariff_normal': 1,
        'is_low_tariff_south': 1}
    
    print(out.get('hourofyear'), out.get('is_dst'))
    assert out == model

def test_utc_60():
    pass

def test_utc_1440():
    pass

def test_cet_15():
    pass

def test_cet_60():
    pass

def test_cet_1440():
    pass

def test_cet_dst_start_15():
    pass

def test_cet_dst_60():
    pass

def test_cet_dst_1440():
    pass

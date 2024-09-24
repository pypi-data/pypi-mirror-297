from andorcal.dst import dst_dates, tz
from zoneinfo import ZoneInfo

from datetime import datetime

def test_dst():
    dt = datetime(2024, 2, 2, 12, tzinfo=ZoneInfo('UTC'))

    dst_dt = dst_dates(dt)

    cet_correct = datetime(2024, 3, 31, 2, tzinfo=tz), datetime(2024, 10, 27, 2, tzinfo=tz)
    cest_correct = datetime(2024, 3, 31, 3, tzinfo=tz), datetime(2024, 10, 27, 2, fold=1, tzinfo=tz)
    
    assert dst_dt.cet() == cet_correct
    assert dst_dt.cest() == cest_correct
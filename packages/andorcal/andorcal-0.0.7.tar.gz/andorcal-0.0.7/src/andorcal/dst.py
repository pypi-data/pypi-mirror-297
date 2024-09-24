from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Optional
import calendar
from andorcal.const import tz


class dst_dates():

    def __init__(self, ymd: Optional[datetime]):
        if ymd is None:
            ymd = datetime.utcnow()
        elif ymd.tzinfo != ZoneInfo('UTC'):
            raise ValueError('provide UTC')

        self.year = ymd.year

        start_day = max(week[-1] for week in calendar.monthcalendar(self.year, 3))
        end_day = max(week[-1] for week in calendar.monthcalendar(self.year, 10))

        self.start = datetime(year=self.year, month=3, day=start_day, hour=1, tzinfo=ZoneInfo('UTC'))
        self.end = datetime(year=self.year, month=10, day=end_day, hour=1, tzinfo=ZoneInfo('UTC'))

        self.is_dst = (ymd >= self.start) and (ymd < self.end)

    def cet(self):
        return (self.start + timedelta(hours=1)).replace(tzinfo=tz), (self.end + timedelta(hours=1)).replace(tzinfo=tz)

    def cest(self):
        return self.start.astimezone(tz), self.end.astimezone(tz)

    def utc(self):
        return self.start, self.end

    # def is_dst(self, time):
    #     """
    #     time must be tz aware"""
    #     if time.tzinfo == ZoneInfo('UTC'):
    #         return (time >= self.start) and (time < self.end)
    #     elif time.tzinfo == ZoneInfo('CET'):
    #         return (time >= self.start.astimezone(tz)) and (time < self.end.astimezone(tz))

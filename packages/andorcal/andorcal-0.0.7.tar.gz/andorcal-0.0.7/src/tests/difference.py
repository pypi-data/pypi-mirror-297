import pytz
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta


old_tz = pytz.timezone('CET')
new_tz = ZoneInfo('CET')
old_utc = pytz.timezone('UTC')
new_utc = ZoneInfo('UTC')

start = datetime(2024, 3, 30, 22, tzinfo=new_tz)
end = datetime(2024, 4, 1, tzinfo=new_tz)

while start <= end:
    print(start.astimezone(new_utc))
    start += timedelta(hours=1)
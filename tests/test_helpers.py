from datetime import datetime
from app.helpers import (
  convert_date_string_to_datetime,
  calculate_follow_duration,
  convert_days_to_years_months_days,
)


def test_convert_date_string_to_datetime():
  dt = convert_date_string_to_datetime('2019-08-07T07:27:30Z')
  assert dt == datetime(2019, 8, 7, 7, 27, 30)

def test_calculate_follow_duration():
  dt = datetime(2014, 12, 3, 0, 8, 41)
  duration = calculate_follow_duration(dt)
  assert type(duration) == str
  assert ':' in duration

def test_convert_days_to_years_months_days():
  ymd = convert_days_to_years_months_days(1708)
  assert ymd == (4, 8, 4)

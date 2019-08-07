from datetime import datetime


def convert_date_string_to_datetime(date_string):
  date_list = date_string.split('T')
  date = date_list[0].split('-')
  time = date_list[1].split(':')
  time[2] = time[2][:-1]
  dt = date
  dt.extend(time)
  dt = [int(dt_val) for dt_val in dt]
  dt = datetime(dt[0], dt[1], dt[2], dt[3], dt[4], dt[5])
  return dt

def calculate_follow_duration(followed_at_datetime):
  duration = datetime.now() - followed_at_datetime
  duration = duration.__str__().split('.')[0]
  return duration

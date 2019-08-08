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

def convert_days_to_years_months_days(days):
  years = days // 365
  days = days % 365
  months = int(days / 30.44)
  days = int(days % 30.44)
  return (years, months, days)

def build_follow_duration_string(followed_at):
  followed_at_dt = convert_date_string_to_datetime(followed_at)
  duration = calculate_follow_duration(followed_at_dt)
  duration_str = ''
  if 'days' in duration:
    days = int(duration.split()[0])
    ymd = convert_days_to_years_months_days(days)
    duration_str = f'{ymd[0]} years, {ymd[1]} months, {ymd[2]} days, '
  time = duration.split()[-1]
  time = [int(num) for num in time.split(':')]
  duration_str += f'{time[0]} hours, {time[1]} minutes, {time[2]} seconds'
  return duration_str

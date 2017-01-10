#!/usr/bin/env python
# coding: utf-8

from datetime import datetime, timedelta, timezone

'''
datetime是python内置的时间处理模块
calendar是历法模块（以西历为准）
timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0,
    hours=0, weeks=0)可对时间进行加减天数和小时数等的计算
'''

# 当前时间
now = datetime.now()
print(now)
print(type(now))

# 获取指定日期和时间的datetime(year, month, day, hour, minute, second)格式
dt = datetime(2016, 12, 30, 6, 48, 23)
print(dt)

# 当前时间戳
print(datetime.utcnow())

# datetime to UTC时间戳timestamp
print(dt.timestamp())

# timestamp to datetime
print(datetime.fromtimestamp(dt.timestamp())) # 本地时区时间
print(datetime.utcfromtimestamp(dt.timestamp())) # 0区时

# 字符串型时间数据('%Y-%m-%d %H:%M:%S')转换为datetime
# https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
cday = datetime.strptime('2016-9-11 18:19:59', '%Y-%m-%d %H:%M:%S')
print(cday)

# datetime to str
print(now.strftime('%a, %b %d %H:%M'))

# timedelta
print(now + timedelta(hours=10))
print(now + timedelta(days=3, hours=8))

# 时区转换
def tz_utc(hours=0, minutes=0):
    '默认为0时区;时区范围为-11~12;以及可选分钟'
    return timezone(timedelta(hours=hours, minutes=minutes))

# 拿到本机UTC时间并转换为0时区
utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
print(utc_dt)

bj_dt = utc_dt.astimezone(tz_utc(8, 30))
print(bj_dt)

msk_dt = bj_dt.astimezone(tz_utc(3))
print(msk_dt)

def to_timestamp(dt_user, tz_user):
    import re
    dt_datetime = datetime.strptime(dt_user, '%Y-%m-%d %H:%M:%S')
    tz_match = re.match(r'^UTC([+-]?\d+):(\d+)', tz_user)
    tz_user_utc = tz_utc(int(tz_match.group(1)), int(tz_match.group(2)))
    dt_datetime_user = dt_datetime.replace(tzinfo=tz_user_utc)
    return dt_datetime_user.timestamp()

dt_user = '2015-1-21 9:01:30'
tz_user = 'UTC+5:00'
print(to_timestamp(dt_user, tz_user))
tz_user1 = 'UTC5:00'
print(to_timestamp(dt_user, tz_user1))

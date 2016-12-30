#!/usr/bin/env python
# coding: utf-8

from datetime import datetime, timedelta

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

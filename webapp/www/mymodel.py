# coding:utf-8

import time
import uuid
from myorm import *

def next_id():
    return "%015d%s000" % (int(time.time() * 1000), uuid.uuid4().hex)

'''
日期和时间用float类型存储在数据库中，而不是datetime类型，这么做的好处是不必关心数据库
的时区以及时区转换问题，排序非常简单，显示的时候，只需要做一个float到str的转换，也非常容易。
'''
class User(Model):
    __table__ = 'users'

    id = StringField(primary_key=True, default=next_id, length=50)
    email = StringField(length=50)
    passwd = StringField(length=50)
    admin = BooleanField()
    name = StringField(length=50)
    image = StringField(length=500)
    created_at = FloatField(default=time.time)


class Blog(Model):
    __table__ = 'blogs'

    id = StringField(primary_key=True, default=next_id, length=50)
    user_id = StringField(length=50)
    user_name = StringField(length=50)
    user_image = StringField(length=500)
    name = StringField(length=50)
    summary = StringField(length=200)
    content = TextField()
    created_at = FloatField(default=time.time)


class Comment(Model):
    __table__ = 'comments'

    id = StringField(primary_key=True, default=next_id, length=50)
    blog_id = StringField(length=50)
    user_id = StringField(50)
    user_name = StringField(50)
    user_image = StringField(500)
    content = TextField()
    created_at = FloatField(default=time.time)

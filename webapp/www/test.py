#!/usr/bin/env python3
# coding:utf-8

import myorm
import asyncio
import sys
import logging;logging.basicConfig(level=logging.INFO)
from mymodel import User, Blog, Comment

async def test():
    await myorm.create_pool(user='www-data', password='www-data',
                            db='awesome', loop=loop)
    for i in range(0, 1000):
        name = 'Test{0}'.format(i)
        email = 'test%{0}@python.com'.format(i)
        passwd = '12345python{0}'.format(i)
        image = 'image{0}'.format(i)
        u = User(name=name, email=email, passwd=passwd,
             image=image)
        await u.save()
    await myorm.destory_pool()
    logging.info('test ok')

loop = asyncio.get_event_loop()
loop.run_until_complete(test())

loop.close()
if loop.is_closed():
    sys.exit(0)

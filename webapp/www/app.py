import logging; logging.basicConfig(level=logging.INFO)
import asyncio
import os
import json
import time
import aiomysql
from datetime import datetime
from aiohttp import web
from myorm import *


class User(Model):
    __table__ = 'users'
    id = IntegerField(primary_key=True)
    name = StringField()


def index(request):
    return web.Response(body=b'<h1>Awsome</h1>', content_type='text/html', charset='UTF-8')

async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()

if __name__ == "__main__":
    user = User(id=123, name='Michael')
    print(user['id'])

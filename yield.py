#!/usr/bin/env python
#coding:utf-8

import asyncio

'''
协程，又称微线程，纤程。英文名Coroutine。
asyncio是Python 3.4版本引入的标准库，直接内置了对异步IO的支持。
用asyncio提供的@asyncio.coroutine可以把一个generator标记为coroutine类型，
然后在coroutine内部用yield from调用另一个coroutine实现异步操作

为了简化并更好地标识异步IO，从Python 3.5开始引入了新的语法async和await，可以让coroutine的代码更简洁易读
'''
def consumer():
    r = ''
    while True:
        n = yield r
        print('>>>c.n %d' % n)
        print('[CONSUMER] consuming %s...' % n)
        r = '200 OK'

def produce(c):
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()

c = consumer()
produce(c)

# 把一个generator标记为coroutine类型
@asyncio.coroutine
def wget(host):
    print('wget %s ..' % host)
    connect = asyncio.open_connection(host, 80)
    reader, writer = yield from connect
    header = 'GET / HTTP/1.0\r\nHost:%s \r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    yield from writer.drain()
    while True:
        line = yield from reader.readline()
        if line == b'\r\n':
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
    writer.close()


loop = asyncio.get_event_loop()
tasks = [wget(host) for host in ['www.sina.com.cn',
                                 'www.sohu.com',
                                 'www.zhihu.com']]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
'''
async def awget(host):
    print('wget %s ..' % host)
    connect = asyncio.open_connection(host, 80)
    reader, writer = await connect
    header = 'GET / HTTP/1.0\r\nHost:%s \r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    await writer.drain()
    while True:
        line = await reader.readline()
        if line == b'\r\n':
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
    writer.close()
loop1 = asyncio.get_event_loop()
task1 = [awget(host) for host in ['www.sina.com.cn',
                                 'www.sohu.com',
                                 'www.zhihu.com']]
loop1.run_until_complete(asyncio.wait(task1))
loop1.close()
'''

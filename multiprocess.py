#!/usr/bin/env python
## -*- coding:utf-8 -*-

'''
一次进程(process)至少有一个线程(thread)；线程是最小的执行单元
多进程、多线程需要着重处理数据同步和共享问题。
'''

# multiprocessing 多进程
# fork() in unix os

import os
import time
import random
import subprocess
from multiprocessing import Process, Pool, Queue

if hasattr(os, 'fork'):
    print('unix fork()>>>>>>>>>>>>>')
    print('Process (%s) start...' % os.getpid())
    pid = os.fork()
    if pid == 0:
        print('child process (%s); and parent is %s.' % (os.getpid(), os.getppid()))
    else:
        print('%s created child process (%s).' % (os.getpid(), pid))

# python model:multiprocessing

def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))


def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))

def write(q):
    print('Process to write: %s' % os.getpid())
    for value in ['A', 'B', 'C']:
        print('Put %s to queue...' % value)
        q.put(value)
        time.sleep(random.random())

def read(q):
    print('Process to read: %s' % os.getpid())
    while True:
        value = q.get(True)
        print('Get %s from queue.' % value)

if __name__ == '__main__':
    print('\npython multiprocessing>>>>>>>>>>>>>>>>>>>>>')
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('child process will start.')
    p.start()
    p.join()
    print('Child process end.')

    time.sleep(1)
    print('Parent process %s. with pool>>>>>>>>>>>>>>>' % os.getpid())
    p = Pool(8)
    for i in range(8):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocessses done.')

    print('$ nslookup www.python.org')
    r = subprocess.call(['nslookup', 'www.python.org'])
    print('Exit code:', r)

    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    pw.start()
    pr.start()
    pw.join()
    # pr是死循环，无法等待时强行结束
    pr.terminate()

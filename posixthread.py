#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import threading

def loop():
    print('thread %s is running...' % threading.current_thread().name)
    n = 0
    while n < 5:
        n = n + 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)
    print('thread %s ended.' % threading.current_thread().name)

print('thread %s is running...' % threading.current_thread().name)
t = threading.Thread(target=loop)
t.start()
t.join()
print('thread %s ended.' % threading.current_thread().name)


# 多线程的锁；python在设计时使用的是全局锁的机制，故而无法实现多线程并

balance = 0

def change_it(n):
    global balance
    balance = balance + n
    balance = balance - n

def run_thread(n):
    for i in range(100000):
        change_it(n)

t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
t1.start()
t2.start()
t1.join()
t1.join()
print(balance)

time.sleep(1)
balance = 0
lock = threading.Lock()

def run_lock_thread(n):
    for i in range(100000):
        lock.acquire()
        try:
            change_it(n)
        finally:
            lock.release()

l1 = threading.Thread(target=run_lock_thread, args=(5,))
l2 = threading.Thread(target=run_lock_thread, args=(8,))
l1.start()
l2.start()
l1.join()
l2.join()
print(balance)

time.sleep(1)
# ThreadLocl用于管理每个线程内部多个函数参数的传递问题
local_school = threading.local()

def process_student():
    std = local_school.student
    print("hello, %s in ( %s )" % (std, threading.current_thread().name))

def process_thread(name):
    local_school.student = name
    process_student()

s1 = threading.Thread(target=process_thread, args=('Alice',), name='Thread-a')
s2 = threading.Thread(target=process_thread, args=('python',), name='Thread-b')
s1.start()
s2.start()
s1.join()
s2.join()

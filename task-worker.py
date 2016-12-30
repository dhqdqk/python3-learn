#!/usr/bin/env python
# coding:utf-8

import time
import sys
import queue
from multiprocessing.managers import BaseManager

'''
分布式工作进程
1.先注册队列get_task_queue和get_result_queue
'''

class QueueManager(BaseManager):
    pass

class BaseWorker(object):
    def __init__(self, server, port, authkey):
        self.server = server
        self.port = port
        self.authkey = authkey

    def regist_queue(self):
        pass

    def connect(self):
        print("Connect to server %s ..." % self.server)
        self.regist_queue()
        self.m = QueueManager(address=(self.server, self.port), authkey=self.authkey)
        self.m.connect()
        self.task = self.m.get_task_queue()
        self.result = self.m.get_result_queue()

    def work(self):
        pass


if __name__ == "__main__":
    class TestWorker(BaseWorker):
        def __init__(self, server='127.0.0.1', port=5000, authkey=b'abc'):
            super(TestWorker, self).__init__(server, port, authkey)

        def regist_queue(self):
            QueueManager.register('get_task_queue')
            QueueManager.register('get_result_queue')

        def work(self):
            for i in range(20):
                try:
                    n = self.task.get(timeout=1)
                    print('run task %d * %d...' % (n, n))
                    r = '%d + %d = % d' % (n, n, n*n)
                    time.sleep(1)
                    self.result.put(r)
                except queue.Empty:
                    print('task queue is empty.')


    test = TestWorker()
    test.connect()
    test.work()
    print('Worker exit...')

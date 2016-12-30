#!/usr/bin/env python
# coding:utf-8

import multiprocessing
import random
import time
import queue
from multiprocessing.managers import BaseManager

'''
managers子模块支持将多进程分布到多台机器上
queue.Queue用于管理多进程之间的通信
任务队列的数据储存于task_queue；
结果队列的数据储存于result_queue；
读取结果时按序读取；类似于列表
'''

class QueueManager(BaseManager):
    pass

class BaseMaster(object):
    '''
    分类式管理器的抽象基类，必要的参数为IP地址，端口号，验证码；
    sendtask()用于自定义发放任务；getresult()自定如何从结果队列中获取结果的行为；
    start()用于创建队列，连接网络并启动管理器；并创建连接队列的两个变量self.task, self.result
    '''
    def __init__(self, address, port, authkey):
        self.address = address
        self.port = port
        self.authkey = authkey

    def sendtask(self):
        pass

    def getresult(self):
        pass

    def create_queue(self):
        pass

    def regist_queue(self):
        pass

    def start(self):
        self.create_queue()
        self.regist_queue()
        self.manager = QueueManager(address=(self.address, self.port), authkey=self.authkey)
        self.manager.start()
        self.task = self.manager.get_task_queue()
        self.result = self.manager.get_result_queue()

    def shutdown(self):
        self.manager.shutdown()
        print('master exit.')


if __name__ == '__main__':
    class TestMaster(BaseMaster):
        def __init__(self, address='', port=5000, authkey=b'abc'):
            super(TestMaster, self).__init__(address, port, authkey)

        def create_queue(self):
            self.task_queue = queue.Queue()
            self.result_queue = queue.Queue()

        def regist_queue(self):
            QueueManager.register('get_task_queue', callable=lambda: self.task_queue)
            QueueManager.register('get_result_queue', callable=lambda: self.result_queue)

        def sendtask(self):
            print('Try get results...')
            for i in range(20):
                n = random.randint(0, 10000)
                print('Put task %d...' % n )
                self.task.put(n)

        def getresult(self):
            print('Try get results...')
            for i in range(20):
                r = self.result.get(timeout=10)
                print('Result: %s' % r)

    test = TestMaster()
    test.start()
    test.sendtask()
    test.getresult()
    test.shutdown()

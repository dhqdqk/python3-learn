#!/usr/bin/env python
## -*- coding: utf-8 -*-

'''
test the codes: Error, Log, unittest
'''

# Error Type
import logging
#logging.basicConfig(level=logging.INFO)

def foo(s):
    return 10 / int(s)

def bar(s):
    return foo(s) * 2

def err():
    try:
        bar('0')
    except Exception as e:
        logging.exception(e)

'''
单元测试：以测试为驱动的开发模式
编写单元测试，需要引入Python自带的unittest模块.

文档测试：doc说明中可以带上示例代码及出错信息，用于表明正确的使用方法
'''
class Dict(dict):
    '''
    Simple dict but also support access as x.y style.

    >>> d1 = Dict()
    >>> d1['x'] = 100
    >>> d1.x
    100
    >>> d1.y = 200
    >>> d1['y']
    200
    >>> d2 = Dict(a=1, b=2, c='3')
    >>> d2.c
    '3'
    >>> d2['empty']
    Traceback (most recent call last):
        ...
    KeyError: 'empty'
    >>> d2.empty
    Traceback (most recent call last):
        ...
    AttributeError: 'Dict' object has no attribute 'empty'
    '''
    def __init__(self, **kw):
        super().__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

import unittest

class TestDict(unittest.TestCase):

    def test_init(self):
        d = Dict(a=1, b='test')
        self.assertEqual(d.a, 1)
        self.assertEqual(d.b, 'test')
        self.assertTrue(isinstance(d, dict))

    def test_key(self):
        d = Dict()
        d['key'] = 'value'
        self.assertEqual(d.key, 'value')

    def test_attr(self):
        d = Dict()
        d.key = 'value'
        self.assertTrue('key' in d)
        self.assertEqual(d['key'], 'value')

    def test_keyerror(self):
        d = Dict()
        with self.assertRaises(KeyError):
            value = d['empty']

    def test_attrerror(self):
        d = Dict()
        with self.assertRaises(AttributeError):
            value = d.empty

# 文档测试
def fact(n):
    '''
    >>> fact(1)
    1
    >>> fact(2)
    2
    >>> fact(5)
    120
    >>> fact(0)
    Traceback (most recent call last):
    ...
    ValueError
    '''
    if n<1:
        raise ValueError()
    if n==1:
        return 1
    return n*fact(n-1)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    unittest.main()
    d = Dict()
    print(d['empty'])

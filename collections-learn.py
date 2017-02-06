#!/usr/bin/env python
# coding:utf-8

from collections import namedtuple, deque, defaultdict, OrderedDict, Counter

'''
collections提供许多具有数学集合概念的数据处理功能，为集合类的数据
'''

# 构造tuple对象的集合
# 构造坐标
point = namedtuple('Point', ['x', 'y'])
p = point(1, 2)
print(p.x, p.y)

# 构造圆
circle = namedtuple('Circle', ['x', 'y', 'r'])
c = circle(1, 2, 3)
print(c.x, c.y, c.r)

# deque为具有高效实现插入和删除元素的双向列表；适合于队列和栈；
#　list按索引访问高效，但插入和删除操作低效
q = deque(['a', 'b', 'c'])
q.append('x')
q.appendleft('y')
print(q)
q.popleft()
print(q)

# defaultdict会自动给不存在的key访问返回一个默认的值（数据中不会添加）
dd = defaultdict(lambda: '无')
dd['key1'] = 'abc'
print(dd['key1'])
print(dd['key2'])

# OrderedDict会构建一个key有序的字典对象；但插入对象时则按插入顺序排列，不进行key重排
# Counter是一个简单的计数器，例如，统计字符出现的个数
c = Counter()
for i in 'programming python':
    c[i] = c[i] + 1
print(c)
print(Counter('programmming golang'))
